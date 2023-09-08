import random

class RandMMU:
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
        self.frames = frames
        self.page_table = {}  # Dictionary to keep track of loaded pages
        self.debug_mode = False
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        random.seed(0)

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        if page_number in self.page_table:
            if self.debug_mode:
                print(f"Page {page_number} is already in memory.")
        else:
            self.page_faults += 1
            if len(self.page_table) >= self.frames:
                # Choose a random page to replace
                page_to_replace = random.choice(list(self.page_table.keys()))
                # If the replaced page was dirty, increment disk writes
                if self.page_table[page_to_replace] == "W":
                    self.disk_writes += 1
                del self.page_table[page_to_replace]
                if self.debug_mode:
                    print(f"Replacing page {page_to_replace}.")

            # Load the new page into memory
            self.page_table[page_number] = "R"
            if self.debug_mode:
                print(f"Loading page {page_number} into memory.")

    def write_memory(self, page_number):
        if page_number in self.page_table:
            self.page_table[page_number] = "W"
            if self.debug_mode:
                print(f"Marking page {page_number} as dirty.")
        else:
            self.page_faults += 1
            if len(self.page_table) >= self.frames:
                # Choose a random page to replace (same logic as read_memory)
                page_to_replace = random.choice(list(self.page_table.keys()))
                if self.page_table[page_to_replace] == "W":
                    self.disk_writes += 1
                del self.page_table[page_to_replace]
                if self.debug_mode:
                    print(f"Replacing page {page_to_replace}.")

            # Load the new page into memory
            self.page_table[page_number] = "W"
            if self.debug_mode:
                print(f"Loading page {page_number} into memory as dirty.")

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults