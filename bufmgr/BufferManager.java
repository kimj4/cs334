import java.io.*;
import java.util.Arrays;
import java.util.HashMap;

/**
 * Buffer manager. Manages a memory-based buffer pool of pages.
 * @author Dave Musicant, with considerable material reused from the
 * UW-Madison Minibase project
 */
public class BufferManager
{
    public static class PageNotPinnedException
        extends RuntimeException {};
    public static class PagePinnedException extends RuntimeException {};

    /**
     * Value to use for an invalid page id.
     */
    public static final int INVALID_PAGE = -1;

    private static class FrameDescriptor
    {
        private int pageNum;
        private String fileName;
        private int pinCount;
        private boolean dirty;
        private boolean referenced;

        public FrameDescriptor()
        {
            pageNum = INVALID_PAGE;
            pinCount = 0;
            fileName = null;
            dirty = false;
            referenced = true;
        }

    }

    // Here are some private variables to get you started. You'll
    // probably need more.
    private Page[] bufferPool;
    private FrameDescriptor[] frameTable;
    private int clockPosition;
    private HashMap<Integer, Integer> map;

    /**
     * Creates a buffer manager with the specified size.
     * @param poolSize the number of pages that the buffer pool can hold.
     */
    public BufferManager(int poolSize)
    {
        bufferPool = new Page[poolSize];
        frameTable = new FrameDescriptor[poolSize];
        clockPosition = 0;
        map = new HashMap<Integer, Integer>();
        initialize();
    }

    /**
     * initializes every element in both bufferPool and frameTable
     */
    private void initialize() {
        for (int i = 0; i < poolSize(); i++) {
            bufferPool[i] = new Page();
        }
        for (int j = 0; j < poolSize(); j++) {
            frameTable[j] = new FrameDescriptor();
        }
    }

    /**
     * Returns the pool size.
     * @return the pool size.
     */
    public int poolSize()
    {
        return bufferPool.length;
    }

    /**
     * runs the clock hand as specified and returns the position in the
     * bufferpool that is available to be removed
     * @return returns the position of the table that can be freed
     */
    private int clock() {
        boolean done = false;
        int returnidx = -1;
        int idx;
        int initialClockPosition = clockPosition;
        while (!done) {

            idx = clockPosition % (poolSize());
            // if nothing has been written in the frame, return it
            // if (frameTable[idx].fileName == null) {
            //     returnidx = idx;
            // } else {
                if (frameTable[idx].pinCount == 0) {
                    if (frameTable[idx].referenced == false) {
                        returnidx = idx;
                        if (frameTable[idx].dirty == true){
                            try {
                                flushPage(frameTable[idx].pageNum, frameTable[idx].fileName);
                            }
                            catch (IOException e) {
                                System.out.println("failure while flushing block");
                            }
                        }
                      // if frame is not pinned and referenced is true, set
                      //  referenced to false
                    } else {
                        frameTable[idx].referenced = false;
                    }
                }
            // }
            // if the returnidx has been changed, delete previous reference
            //  to that frame slot in the map
            // if the clock went around two cycles without finding anything,
            //  return -1;
            if (clockPosition == (initialClockPosition + (2 * (poolSize())))) {
                done = true;
                // clockPosition++;
            } else if (returnidx != -1) {
                done = true;
                map.values().remove(returnidx);
                clockPosition++;
            } else {
                clockPosition++;
            }

        }
        return returnidx;
    }

    /**
     * Checks if this page is in buffer pool. If it is, returns a
     * pointer to it. Otherwise, it finds an available frame for this
     * page, reads the page, and pins it. Writes out the old page, if
     * it is dirty, before reading.
     * @param pinPageId the page id for the page to be pinned
     * @param fileName the name of the database that contains the page
     * to be pinned
     * @param emptyPage determines if the page is known to be
     * empty. If true, then the page is not actually read from disk
     * since it is assumed to be empty.
     * @return a reference to the page in the buffer pool. If the buffer
     * pool is full, null is returned.
     * @throws IOException passed through from underlying file system.
     */
    public Page pinPage(int pinPageId, String fileName, boolean emptyPage)
        throws IOException
    {
        // if the page is already in pool, increment pincount
        if (map.get(pinPageId) != null) {
            frameTable[map.get(pinPageId)].pinCount++;
            return bufferPool[map.get(pinPageId)];
        // if not, load it into pool
        } else {
            int emptySlot = clock();
            // map.put(pinPageId, emptySlot);
            // if there is an available frame
            if (emptySlot != -1) {
                map.put(pinPageId, emptySlot);
                DBFile dbFile = new DBFile(fileName);
                if (!emptyPage) {
                    // checking if the contents of the frame changed
                    byte[] tempArray = new byte[poolSize()];
                    System.arraycopy(bufferPool[map.get(pinPageId)].data, 0,
                                     tempArray, 0, poolSize() );
                    dbFile.readPage(pinPageId, bufferPool[map.get(pinPageId)]);
                    if (!Arrays.equals(tempArray, bufferPool[map.get(pinPageId)].data)) {
                        frameTable[map.get(pinPageId)].dirty = true;
                    }
                }
                frameTable[map.get(pinPageId)].pinCount++;
                frameTable[map.get(pinPageId)].pageNum = pinPageId;
                frameTable[map.get(pinPageId)].fileName = fileName;
                return bufferPool[map.get(pinPageId)];
            } else {
                return null;
            }
        }
    }

    /**
     * If the pin count for this page is greater than 0, it is
     * decremented. If the pin count becomes zero, it is appropriately
     * included in a group of replacement candidates.
     * @param unpinPageId the page id for the page to be unpinned
     * @param fileName the name of the database that contains the page
     * to be unpinned
     * @param dirty if false, then the page does not actually need to
     * be written back to disk.
     * @throws PageNotPinnedException if the page is not pinned, or if
     * the page id is invalid in some other way.
     * @throws IOException passed through from underlying file system.
     */
    public void unpinPage(int unpinPageId, String fileName, boolean dirty)
        throws IOException
    {
        // check that the page exists in pool
        if (map.get(unpinPageId) != null) {
            // check that page is pinned
            if (frameTable[map.get(unpinPageId)].pinCount > 0) {
                frameTable[map.get(unpinPageId)].pinCount--;
                // if the pae is not pinned, mark as referenced
                if (frameTable[map.get(unpinPageId)].pinCount == 0) {
                    frameTable[map.get(unpinPageId)].referenced = true;
                    if (dirty) {frameTable[map.get(unpinPageId)].dirty = true;}
                }
            } else {throw new PageNotPinnedException();}
        } else {throw new PagePinnedException();}
    }


    /**
     * Requests a run of pages from the underlying database, then
     * finds a frame in the buffer pool for the first page and pins
     * it. If the buffer pool is full, no new pages are allocated from
     * the database.
     * @param numPages the number of pages in the run to be allocated.
     * @param fileName the name of the database from where pages are
     * to be allocated.
     * @return an Integer containing the first page id of the run, and
     * a references to the Page which has been pinned in the buffer
     * pool. Returns null if there is not enough space in the buffer
     * pool for the first page.
     * @throws DBFile.FileFullException if there are not enough free pages.
     * @throws IOException passed through from underlying file system.
     */
    public Pair<Integer,Page> newPage(int numPages, String fileName)
        throws IOException
    {
        DBFile dbFile = new DBFile(fileName);
        int firstPageId = dbFile.allocatePages(numPages);
        Page firstPage = pinPage(firstPageId, fileName, false);
        if (map.get(firstPageId) != null) {
            return new Pair(firstPageId, firstPage);
        } else {
            return null;
        }
    }

    /**
     * Deallocates a page from the underlying database. Verifies that
     * page is not pinned.
     * @param pageId the page id to be deallocated.
     * @param fileName the name of the database from where the page is
     * to be deallocated.
     * @throws PagePinnedException if the page is pinned
     * @throws IOException passed through from underlying file system.
     */
    public void freePage(int pageId, String fileName) throws IOException
    {
        DBFile dbFile = new DBFile(fileName);
        if (frameTable[map.get(pageId)].pinCount == 0) {
            dbFile.deallocatePages(pageId, 1);
        } else {
            throw new PagePinnedException();
        }
    }

    /**
     * Flushes page from the buffer pool to the underlying database if
     * it is dirty. If page is not dirty, it is not flushed,
     * especially since an undirty page may hang around even after the
     * underlying database has been erased. If the page is not in the
     * buffer pool, do nothing, since the page is effectively flushed
     * already.
     * @param pageId the page id to be flushed.
     * @param fileName the name of the database where the page should
     * be flushed.
     * @throws IOException passed through from underlying file system.
     */
    public void flushPage(int pageId, String fileName) throws IOException
    {
        DBFile dbFile = new DBFile(fileName);
        if (map.get(pageId) != null) {
            dbFile.writePage(pageId, bufferPool[map.get(pageId)]);
        }
    }

    /**
     * Flushes all dirty pages from the buffer pool to the underlying
     * databases. If page is not dirty, it is not flushed, especially
     * since an undirty page may hang around even after the underlying
     * database has been erased.
     * @throws IOException passed through from underlying file system.
     */
    public void flushAllPages() throws IOException
    {
        for (int key: map.keySet()) {
            if (frameTable[map.get(key)].dirty == true) {
                flushPage(frameTable[map.get(key)].pageNum, frameTable[map.get(key)].fileName);
            }
        }
    }

    /**
     * Returns buffer pool location for a particular pageId. This
     * method is just used for testing purposes: it probably doesn't
     * serve a real purpose in an actual database system.
     * @param pageId the page id to be looked up.
     * @param fileName the file name to be looked up.
     * @return the frame location for the page of interested. Returns
     * -1 if the page is not in the pool.
    */
    public int findFrame(int pageId, String fileName)
    {
      int val = -1;
      for (int i = 0; i < frameTable.length; i++) {
          if (frameTable[i] != null) {
              if (frameTable[i].pageNum == pageId && frameTable[i].fileName == fileName) {
                  val = i;
              }
          }
      }
      return val;
    }
}
