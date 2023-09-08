# this calss implements the clock algorithm for page replacement

class ClockMMU:
    def __init__(self, frames):
        self.clock_hand = 0
        self.use_bit = [] 
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

    def reset_debug(self):
        self.debug = False

    def set_debug(self):
        self.debug = True

    def evict_page(self):
        while self.use_bit[self.clock_hand] != 0:
            self.use_bit[self.clock_hand] = 0  # reset the use bit to 0
            self.clock_hand = (self.clock_hand + 1) % self.frames

        evicted_page = self.cache[self.clock_hand]
        if self.dirty_bits.get(evicted_page, 0) == 1:
            self.writes += 1
            self.dirty_bits[evicted_page] = 0
            if self.debug:
                print(f"Disk write  {evicted_page}")
        else:
            if self.debug:
                print(f"Discard  {evicted_page}")

        return self.clock_hand

    def read_memory(self, page_number):
        if page_number in self.cache:
            self.hits += 1
            self.use_bit[self.cache.index(page_number)] = 1
            if self.debug:
                print(f"reading {page_number}")
        else:
            self.reads += 1
            self.misses += 1
            if self.debug:
                print(f"Page fault  {page_number}")

            if len(self.cache) == self.frames:
                index = self.evict_page()
                self.cache[index] = page_number
                self.use_bit[index] = 1
                self.clock_hand = (self.clock_hand + 1) % self.frames   
            else:
                self.cache.append(page_number)
                self.use_bit.append(1)

            if self.debug:
                print(f"reading {page_number}")

    def write_memory(self, page_number):
        self.dirty_bits[page_number] = 1
        if page_number in self.cache:
            self.hits += 1
            self.use_bit[self.cache.index(page_number)] = 1
            if self.debug:
                print(f"writting {page_number}")
        else:
            self.reads += 1
            self.misses += 1
            if self.debug:
                print(f"Page fault  {page_number}")

            if len(self.cache) == self.frames:
                index = self.evict_page()
                self.cache[index] = page_number
                self.use_bit[index] = 1
                self.clock_hand = (self.clock_hand + 1) % self.frames
            else:
                self.cache.append(page_number)
                self.use_bit.append(1)

            if self.debug:
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
    
