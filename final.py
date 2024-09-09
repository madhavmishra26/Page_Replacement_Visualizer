import tkinter as tk
import random
import time
from collections import deque, defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Page:
    def _init_(self, page_id):
        self.page_id = page_id

class PageReplacementSimulation:
    def __init__(self):
        self.ram_pages = [None] * 8
        self.secondary_memory_pages = [None] * 22
        self.secondary_memory_index = 0
        self.ram_page_index = 0
        self.page_order = deque(maxlen=8)
        self.page_hits = 0
        self.page_misses = 0
        self.page_dict = defaultdict(int)
        self.lengthofword = 0
        self.page_frequency = defaultdict(int)
    

        
class PageReplacementSimulatorGUI:
    def __init__(self, master, simulation):
        self.master = master
        self.simulation = simulation
        self.main_memory_frame = None
        self.secondary_memory_frame = None
        self.buttons = []
        self.temp_char_text = None
        self.stats_label = None
        self.color_dict = {}
        self.available_colors = ["#FFB6C1", "#98FB98", "#87CEEB", "#FFFFE0", "#FFC0CB",
                        "#AFEEEE", "#FFD700", "#D3D3D3", "#DDA0DD", "#00CED1",
                        "#FF8C00", "#7CFC00", "#87CEFA", "#F0E68C", "#FF1493",
                        "#98FB98", "#00FA9A", "#FA8072", "#20B2AA", "#DDA0DD",
                        "#FF6347", "#BA55D3", "#7FFF00", "#87CEEB"]

        self.algorithm_var = tk.StringVar(value="LRU")  # Default algorithm is LRU
        self.is_simulation_running = False
        self.init_ui()
    def get_unique_color(self, char):
        # Ensure that characters are converted to equivalent digits
        if char.isalpha():
            char = str(ord(char.upper()) - ord('A') + 1)

        if char not in self.color_dict:
            color = random.choice(self.available_colors)
            self.color_dict[char] = color
        return self.color_dict[char]
    
    def init_ui(self):
        self.main_memory_frame = tk.Frame(self.master, width=200, height=400, borderwidth=2, relief="solid")
        self.main_memory_frame.grid(row=1, column=0, padx=10, pady=10)
        main_memory_label = tk.Label(self.main_memory_frame, text="Main Memory", font=("Arial", 12, "bold"))
        main_memory_label.grid(row=0, column=0, columnspan=8)
        self.create_buttons(0, 8, self.main_memory_frame, row_offset=1)

        self.secondary_memory_frame = tk.Frame(self.master, width=200, height=800, borderwidth=2, relief="solid")
        self.secondary_memory_frame.grid(row=2, column=0, padx=10, pady=10)
        secondary_memory_label = tk.Label(self.secondary_memory_frame, text="Secondary Memory", font=("Arial", 12, "bold"))
        secondary_memory_label.grid(row=0, column=0, columnspan=8)
        self.create_buttons(8, 30, self.secondary_memory_frame, row_offset=1)
        bottom_frame = tk.Frame(self.master)
        bottom_frame.grid(row=7, column=0, pady=10)
        
        self.temp_char_text = tk.StringVar()
        temp_char_label = tk.Label(self.master, textvariable=self.temp_char_text, font=("Arial", 14))
        temp_char_label.grid(row=3, column=0, pady=10)

        self.stats_label = tk.Label(self.master, text="Page Hits: 0   Page Misses: 0   Available Pages: 8   Occupied Pages: 0",
                                    font=("Arial", 14))
        self.stats_label.grid(row=4, column=0, pady=10)
        input_text_frame = tk.Frame(self.master)
        input_text_frame.grid(row=6, column=0, pady=10)

        self.input_text = tk.StringVar()
        text_field = tk.Entry(input_text_frame, textvariable=self.input_text, width=40, font=("Arial", 14))
        text_field.grid(row=0, column=0)
        
        button_font = ("Arial", 14)

        # Move these lines from their current position inside the init_ui method to the bottom_frame
        lru_button = tk.Button(bottom_frame, text="LRU", command=lambda: self.simulate_algorithm("LRU"), font=button_font)
        lru_button.grid(row=0, column=0, padx=(0, 20), pady=10)

        fifo_button = tk.Button(bottom_frame, text="FIFO", command=lambda: self.simulate_algorithm("FIFO"), font=button_font)
        fifo_button.grid(row=0, column=1, padx=(0, 20), pady=10)

        lfu_button = tk.Button(bottom_frame, text="LFU", command=lambda: self.simulate_algorithm("LFU"), font=button_font)
        lfu_button.grid(row=0, column=2, padx=(0, 20), pady=10)

        reset_button = tk.Button(bottom_frame, text="Reset", command=self.reset_program, font=button_font)
        reset_button.grid(row=0, column=3, padx=(0, 20), pady=10)

        stop_button = tk.Button(bottom_frame, text="Wait 5Sec", command=self.stop_simulation, font=button_font)
        stop_button.grid(row=0, column=4, padx=(0, 20), pady=10)

        random_string_button = tk.Button(bottom_frame, text="Generate Random String", command=self.generate_random_string, font=button_font)
        random_string_button.grid(row=0, column=5,padx=(0, 20), pady=10)
        
        run_button = tk.Button(bottom_frame, text="Run and Plot", command=self.run_simulations_and_plot, font=button_font)
        run_button.grid(row=0, column=6,padx=(0, 20), pady=10)
        
    def stop_simulation(self):
        # Stop the simulation for 5 seconds
        time.sleep(5)  
        
    def create_buttons(self, start, end, frame, row_offset=0):
        for i in range(start, end):
            button_text = f"Page{i + 1}\n" if i < 8 else f"Page{i -7}\n"
            button = tk.Button(frame, text=button_text, bg="white", height=2, font=("Arial", 12))
            button.grid(row=row_offset + i // 8, column=i % 8, padx=5, pady=5)
            self.buttons.append(button)


    def update_button(self, char, index, is_secondary=False):
        color = self.get_unique_color(char)
        if is_secondary==False:
            button = self.buttons[index]
            
            button.configure(text=f"Page{index:X}\n{char}", bg=color)
        if is_secondary:
            secondary_index = index + 8
            secondary_button = self.buttons[secondary_index]
            secondary_button.configure(text=f"Page{index:X}\n{char}", bg=color)

    def simulate_algorithm(self, algorithm):
        input_string = self.input_text.get()  # Get the input string from the entry widget
        if not input_string:
            # If the input string is empty, generate a random string
            input_string = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(30))
            self.input_text.set(input_string)  # Update the entry widget with the generated string
        self.simulation.lengthofword = len(input_string)
        self.simulation.page_frequency.clear()
        self.simulation.page_order = deque(maxlen=8)
        self.simulation.ram_pages = [None] * 8
        self.simulation.secondary_memory_pages = [None] * 22
        for i in range(0,30):
                self.buttons[i].configure(bg="#FFFFFF")
        for char in input_string:
            char=char.upper()
            if algorithm == "LRU":
                
                self.replace_page_lru(char)
            elif algorithm == "FIFO":
                
                self.replace_page_fifo(char)
            elif algorithm == "LFU":
                
                self.replace_page_lfu(char)

            self.master.update()
            time.sleep(.1)

    def replace_page_lru(self, char):
        if char.isalpha():
            page_int = ord(char) - ord('A') + 1
            #print(page_int)
            if 0 <= page_int < 26:  # Adjusted range for hexadecimal digits
                if page_int not in self.simulation.page_order:
                    self.simulation.page_misses += 1
                    self.update_stats_label()

                    if None in self.simulation.ram_pages:
                        # Store in the first available slot in main memory
                        empty_slot = self.simulation.ram_pages.index(None)
                        self.update_button(char, empty_slot)
                        self.update_page_order(page_int)
                        self.simulation.ram_pages[empty_slot] = page_int
                    else:
                        # Check if the page order deque is not empty before popping
                        if self.simulation.page_order:
                            if page_int in self.simulation.secondary_memory_pages:
                                # Store in the first available slot in main memory
                                empty_slot = self.simulation.secondary_memory_pages.index(page_int)
                                # Swap with the least recently used page in main memory
                                lru_page = self.simulation.page_order.popleft()
                                lru_index = self.simulation.ram_pages.index(lru_page)
                                self.simulation.secondary_memory_pages[empty_slot] = lru_page
                                 # Update the buttons for both main and secondary memory
                                
                                self.update_button(chr(lru_page + ord('A') - 1), empty_slot, is_secondary=True)
                                self.update_page_order(page_int)
                                
                                self.simulation.ram_pages[lru_index] = page_int
                                self.update_button(char, lru_index)
                            else:
                                if None in self.simulation.secondary_memory_pages:
                                    empty_slot = self.simulation.secondary_memory_pages.index(None)
                                else:
                                    print("no secondry page is available to swap")
                                    return
                                lru_page = self.simulation.page_order.popleft()
                                lru_index = self.simulation.ram_pages.index(lru_page)
                                #rint("lru_index",lru_index)
                                self.simulation.secondary_memory_pages[empty_slot] = lru_page
                                 # Update the buttons for both main and secondary memory
                                
                                self.update_button(chr(lru_page + ord('A') - 1), empty_slot, is_secondary=True)
                                self.update_page_order(page_int)
                                
                                self.simulation.ram_pages[lru_index] = page_int
                                self.update_button(char, lru_index)
                            
                        else:
                            # Handle the situation when the page order deque is empty
                            # Add the current page to the page order deque
                            self.simulation.page_order.append(page_int)
                else:
                    self.simulation.page_hits += 1
                    self.update_page_order(page_int)
                self.temp_char_text.set(f"Last updated page: {char}")
        else:
            # Handle non-digit characters as needed
            print("please enter characters only")
            pass


    def replace_page_fifo(self, char):
        if char.isalpha():
            page_int = ord(char) - ord('A') + 1
            #print(page_int)
            if 0 <= page_int < 26:  # Adjusted range for hexadecimal digits
                if page_int not in self.simulation.page_order:
                    self.simulation.page_misses += 1
                    self.update_stats_label()

                    if None in self.simulation.ram_pages:
                        # Store in the first available slot in main memory
                        empty_slot = self.simulation.ram_pages.index(None)
                        self.update_button(char, empty_slot)
                        self.update_page_order(page_int)
                        self.simulation.ram_pages[empty_slot] = page_int
                    else:
                        # Check if the page order deque is not empty before popping
                        if self.simulation.page_order:
                            if page_int in self.simulation.secondary_memory_pages:
                                # Store in the first available slot in main memory
                                empty_slot = self.simulation.secondary_memory_pages.index(page_int)
                                #print("sec",self.simulation.secondary_memory_pages)
                                # Swap with the least recently used page in main memory
                                fifo_page = self.simulation.page_order.popleft()
                                fifo_index = self.simulation.ram_pages.index(fifo_page)
                                self.simulation.secondary_memory_pages[empty_slot] = fifo_page
                                 # Update the buttons for both main and secondary memory
                                
                                self.update_button(chr(fifo_page + ord('A') - 1), empty_slot, is_secondary=True)
                                self.update_page_order(page_int)
                                
                                self.simulation.ram_pages[fifo_index] = page_int
                                self.update_button(char, fifo_index)
                            else:
                                if None in self.simulation.secondary_memory_pages:
                                    empty_slot = self.simulation.secondary_memory_pages.index(None)
                                    #print("sec",self.simulation.secondary_memory_pages)
                                else:
                                    print("no secondry page is available to swap")
                                    return
                                fifo_page = self.simulation.page_order.popleft()
                                fifo_index = self.simulation.ram_pages.index(fifo_page)
                                #rint("lru_index",lru_index)
                                self.simulation.secondary_memory_pages[empty_slot] = fifo_page
                                 # Update the buttons for both main and secondary memory
                                
                                self.update_button(chr(fifo_page + ord('A') - 1), empty_slot, is_secondary=True)
                                self.update_page_order(page_int)
                                
                                self.simulation.ram_pages[fifo_index] = page_int
                                self.update_button(char, fifo_index)
                            
                        else:
                            # Handle the situation when the page order deque is empty
                            # Add the current page to the page order deque
                            self.simulation.page_order.append(page_int)
                else:
                    self.simulation.page_hits += 1
                    #self.update_page_order(page_int)
                self.temp_char_text.set(f"Last updated page: {char}")
        else:
            # Handle non-digit characters as needed
            print("please enter characters only")
            pass


    def replace_page_lfu(self, char):
        if char.isalpha():
            page_int = ord(char) - ord('A') + 1

            if 0 <= page_int < 26:
                if page_int not in self.simulation.ram_pages:
                    self.simulation.page_misses += 1
                    self.update_stats_label()

                    if None in self.simulation.ram_pages:
                        # Store in the first available slot in main memory
                        empty_slot = self.simulation.ram_pages.index(None)
                        self.update_button(char, empty_slot)
                        
                        self.simulation.ram_pages[empty_slot] = page_int
                        self.simulation.page_frequency[page_int]=1
                    else:
                        if page_int in self.simulation.secondary_memory_pages:
                            # Store in the first available slot in main memory
                            empty_slot = self.simulation.secondary_memory_pages.index(page_int)
                            # Swap with the least frequently used page in main memory
                            lfu_page = min(self.simulation.ram_pages, key=lambda x: self.simulation.page_frequency[x])

                            # Swap the LFU page with the new page
                            lfu_index = self.simulation.ram_pages.index(lfu_page)
                            self.simulation.secondary_memory_pages[empty_slot] = lfu_page
                            self.update_button(chr(lfu_page + ord('A') - 1), empty_slot, is_secondary=True)
                            

                            # Increment the frequency of the new page
                            self.simulation.page_frequency[page_int] += 1

                            # Decrement the frequency of the replaced LFU page
                            del self.simulation.page_frequency[lfu_page]
                            self.simulation.ram_pages[lfu_index] = page_int
                            self.update_button(char, lfu_index)
                        else:
                            if None in self.simulation.secondary_memory_pages:
                                empty_slot = self.simulation.secondary_memory_pages.index(None)
                            else:
                                print("No secondary page is available to swap")
                                return

                            # Swap the LFU page with the new page
                            lfu_page = min(self.simulation.ram_pages, key=lambda x: self.simulation.page_frequency[x])
                            lfu_index = self.simulation.ram_pages.index(lfu_page)
                            self.simulation.secondary_memory_pages[empty_slot] = lfu_page
                            self.update_button(chr(lfu_page + ord('A') - 1), empty_slot, is_secondary=True)
                            

                            # Increment the frequency of the new page
                            self.simulation.page_frequency[page_int] += 1

                            # Decrement the frequency of the replaced LFU page
                            del self.simulation.page_frequency[lfu_page]
                            self.simulation.ram_pages[lfu_index] = page_int
                            self.update_button(char, lfu_index)

                else:
                    self.simulation.page_hits += 1
                    # Update the frequency of the accessed page
                    self.simulation.page_frequency[page_int] += 1

                self.temp_char_text.set(f"Last updated page: {char}")
            else:
                print("Please enter characters only")
        else:
            # Handle non-alphabetic characters as needed
            print("Please enter characters only")
            
    def update_page_order(self, page):
        if page in self.simulation.page_order:
            self.simulation.page_order.remove(page)
        self.simulation.page_order.append(page)
        #rint(self.simulation.page_order)

    def update_stats_label(self):
        if self.stats_label is None or not self.stats_label.winfo_exists():
        # Check if the stats_label widget is None or has been destroyed
            return
        available_pages = 8 - len(self.simulation.page_order)
        occupied_pages = len(self.simulation.page_order)
        total_requests = self.simulation.page_hits + self.simulation.page_misses
        hit_ratio = (self.simulation.page_hits / total_requests) * 100 if total_requests > 0 else 0
        miss_ratio = (self.simulation.page_misses / total_requests) * 100 if total_requests > 0 else 0

        self.stats_label.config(text=f"Page Hits: {self.simulation.page_hits}   Page Misses: {self.simulation.page_misses}   "
                                     f"Available Pages: {available_pages}   Occupied Pages: {occupied_pages}   "
                                     f"Hit Ratio: {hit_ratio:.2f}%   "
                                     f"Miss Ratio: {miss_ratio:.2f}%")

    def reset_program(self):
        # Destroy the current Tkinter window
        self.master.destroy()

        # Create a new Tkinter window
        root = tk.Tk()
        root.geometry("1080x700")
        root.title("Page Replacement Simulation")

        # Create a new simulation object
        simulation = PageReplacementSimulation()

        # Create a new GUI object with the new simulation
        gui = PageReplacementSimulatorGUI(root, simulation)

        # Start the Tkinter main loop
        root.mainloop()

    def generate_random_string(self):
        random_string =  "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(30))
        self.input_text.set(random_string)
        
    def run_simulations_and_plot(self):
        # Run simulations for LRU, FIFO, and LFU policies
        algorithms = ["LRU", "FIFO", "LFU"]
        results = {"LRU": [], "FIFO": [], "LFU": []}

        for algorithm in algorithms:
            # Run simulation for the current algorithm
            self.simulate_algorithm(algorithm)
            # Store simulation results
            results[algorithm].append((self.simulation.page_hits, self.simulation.page_misses))
            self.simulation.ram_pages = [None] * 8
            self.simulation.secondary_memory_pages = [None] * 22
            self.simulation.page_hits = 0
            self.simulation.page_misses = 0
            print("Debug: Results =", results)
            #print("afterReset",self.simulation.secondary_memory_pages)
            for i in range(0,30):
                self.buttons[i].configure(bg="#FFFFFF")
        # Plotting results in a new window
        self.plot_results(results)
            
    def plot_results(self, results):
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Simulation Results")

        # Create a Matplotlib figure
        fig = Figure(figsize=(8, 6), dpi=100)
        plot_area = fig.add_subplot(111)

        # Generate some example data for the x-axis (here, just using algorithm names)
        algorithms = list(results.keys())
        x_positions = np.arange(len(algorithms))

        # Plot page hits and misses for each algorithm
        hits_data = [result[0][0] for result in results.values()]
        misses_data = [result[0][1] for result in results.values()]
        # Before the bar function calls
        print("hits_data:", hits_data)
        print("misses_data:", misses_data)

        plot_area.bar(x_positions - 0.2, hits_data, width=0.4, label="Page Hits")
        plot_area.bar(x_positions + 0.2, misses_data, width=0.4, label="Page Misses")

        # Set plot labels and legend
        plot_area.set_xticks(x_positions)
        plot_area.set_xticklabels(algorithms)
        plot_area.set_ylabel("Count")
        plot_area.set_title("Page Replacement Policy Comparison")
        plot_area.legend()

        # Create a canvas to embed Matplotlib plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1080x700")
    root.title("Page Replacement Simulation")

    simulation = PageReplacementSimulation()
    gui = PageReplacementSimulatorGUI(root, simulation)

    root.mainloop()