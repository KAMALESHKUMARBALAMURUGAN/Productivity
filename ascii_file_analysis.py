import matplotlib.pyplot as plt

def filter_asc_file(input_file, output_file, target_id):
    print(f"Filtering file for target ID {target_id}...")
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        previous_time = None
        count_greater_than_one = 0
        times = []
        # sequence_count_00 = 0
        # sequence_count_01 = 0
        # # target_sequence_00 = "00 00 00 00 00 00 00 00"
        # # target_sequence_01 = "01 00 00 00 00 00 00 00"
        
        for line in infile:
            columns = line.split()
            if len(columns) > 2 and columns[2] == target_id:
                current_time = float(columns[0])
                times.append(current_time)
                
                if previous_time is not None:
                    time_diff = current_time - previous_time
                    if time_diff > 1:
                        # print("previous_time:", previous_time)
                        # print("current_time:", current_time)
                        # print(f"Time difference greater than 1: {time_diff}")
                        count_greater_than_one += 1
                    outfile.write(f"{line.strip()} {time_diff:.6f}\n")
                else:
                    outfile.write(f"{line.strip()} 0.000000\n")
                
                previous_time = current_time
                
                # # Check for the target sequences
                # if target_sequence_00 in line:
                #     sequence_count_00 += 1
                # if target_sequence_01 in line:
                #     sequence_count_01 += 1
        
        print(f"Number of times the time difference is greater than 1: {count_greater_than_one}")
        # print(f"Number of times the sequence '{target_sequence_00}' appears: {sequence_count_00}")
        # print(f"Number of times the sequence '{target_sequence_01}' appears: {sequence_count_01}")
    
    # Plotting the time column
    plt.plot(times)
    plt.xlabel('Index')
    plt.ylabel('Time')
    plt.title(f'Time Plot for ID {target_id}')
    # plt.show()

if __name__ == "__main__":
    input_file = r'C:\Users\kamalesh.kb\Nduro\ISSUE_4_MAR_25\Nduro 2.3 kWh V-25 _04-03-2025_ Eco mode_Highway_B.no-76_time_06.48 pm to_09.27 pm.asc'  # Replace with your input file path
    output_file = 'cleaned.asc'
    target_id = '00000008x'
    
    filter_asc_file(input_file, output_file, target_id)