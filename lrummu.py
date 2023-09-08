class LruMMU:
    def __init__(self, frames):
        self.frames = frames
        self.reads = 0
        self.writes = 0
        self.debug = False
        # variables for the TLB
        self.cache = []
        self.hits = 0
        self.misses = 0
        self.evict = 0
        self.dirty_bits = {}


    def set_debug(self):
        # todo: implement the set_debug method
        self.debug = True

    def reset_debug(self):
        # todo: implement the reset_debug method
        self.debug = False

    # def read_memory(self, page_number):
    #     # todo: implement the read_memory method
        
    #     # if the page is in the cache, then its a hit
    #     if page_number in self.cache:
    #         self.hits += 1
    #         # move the page to the end and remove the instance of it that is already in there
    #         self.cache.remove(page_number)
    #         self.cache.append(page_number)
    #     else:
    #         # if it is a miss
    #         self.misses += 1
    #         self.reads += 1

    #     if len(self.cache) == self.frames:
    #         evicted_page = self.cache.pop(0)
    #         if self.dirty_bits.get(evicted_page, 0) == 1:
    #             self.writes += 1  # Increment disk writes only if the evicted page is dirty

    #         self.cache.append(page_number)

    #         if self.debug: 
    #             print(f"Page fault {page_number}")
    #             print(f"reading {page_number}")

    # def write_memory(self, page_number):
    #     self.dirty_bits[page_number] = 1  # Set the dirty bit for this page

    #     # if the page is in the cache, then it's a hit
    #     if page_number in self.cache:
    #         self.hits += 1
    #         self.cache.remove(page_number)
    #         self.cache.append(page_number)
    #     else:
    #         # if it is a miss
    #         self.misses += 1

    #         # Check for eviction
    #         if len(self.cache) == self.frames:
    #             evicted_page = self.cache.pop(0)
    #             if self.dirty_bits.get(evicted_page, 0) == 1:
    #                 self.writes += 1  # Increment disk writes only if the evicted page is dirty

    #         self.cache.append(page_number)

    def read_memory(self, page_number):
        # if the page is in the cache, then it's a hit
        if page_number in self.cache:
            self.hits += 1
            # move the page to the end and remove the instance of it that is already in there
            self.cache.remove(page_number)
            self.cache.append(page_number)
        else:
            # if it is a miss
            self.misses += 1
            self.reads += 1  # Increment disk reads

            # Check for eviction and possible disk write
            if len(self.cache) == self.frames:
                evicted_page = self.cache.pop(0)
                if self.dirty_bits.get(evicted_page, 0) == 1:
                    self.writes += 1  # Increment disk writes only if the evicted page is dirty
                    self.dirty_bits[evicted_page] = 0
                    if self.debug:
                        print(f"Disk Write {page_number}")

            self.cache.append(page_number)
            if self.debug: 
                print(f"Page fault {page_number}")
                print(f"reading {page_number}")

    def write_memory(self, page_number):
        self.dirty_bits[page_number] = 1  # Set the dirty bit for this page

        # if the page is in the cache, then it's a hit
        if page_number in self.cache:
            self.hits += 1
            self.cache.remove(page_number)
            self.cache.append(page_number)
        else:
            # if it is a miss
            self.misses += 1
            self.reads += 1

            # Check for eviction and possible disk write
            if len(self.cache) == self.frames:
                evicted_page = self.cache.pop(0)
                if self.dirty_bits.get(evicted_page, 0) == 1:
                    self.writes += 1  # Increment disk writes only if the evicted page is dirty
                    self.dirty_bits[evicted_page] = 0

            self.cache.append(page_number)

            if self.debug: 
                print(f"Page fault {page_number}")
                print(f"writting {page_number}")


    def get_total_disk_reads(self):
        # todo: implement the get_total_disk_reads method
        return self.reads
    
    def get_total_disk_writes(self):
        # todo: implement the gettotal_disk_writes method
        return self.writes

    def get_total_page_faults(self):
        # todo: implement the get_total_page_faults method
        return self.misses
    

