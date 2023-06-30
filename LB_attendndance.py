import re
import matplotlib.pyplot as plt
from collections import defaultdict

month_mapping = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

def flatten_dict(d):
    flattened_dict = {}
    for key, value in d.items():
        if isinstance(value, defaultdict):
            flattened_dict[key] = flatten_dict(dict(value))
        else:
            flattened_dict[key] = value
    return flattened_dict

def parse_whatsapp_messages(file_path):
    #attendance = defaultdict(lambda: defaultdict(int))
    Kannada_pattern = r"ಶುಭೋದಯಗಳು, ಶುಭೋದಯ, ಸುಭೋದಯಗಳು"
    # Regular expression pattern to search for Kannada strings
    Kannada_upattern = r"[\u0C80-\u0CFF]+"
    
    attendance = defaultdict(int)
    current_month = None

    with open(file_path, 'r', encoding='utf-8') as file:
        pattern = r'\d{2}/(\d{2})/\d{2},'
        for line in file:
            # Check for new month
            if re.match(pattern, line):
                current_month = re.findall(pattern, line)[0]
                
            # Check for good morning messages
            if re.search(r'good\s+morning|gm|suprabhatam|Suprabhatham|Shubodaya|Shubodhaya|Gud\s+morning|Gud\s+Mrng', line, re.IGNORECASE):
                sender = re.findall(r'\d{2}/\d{2}/\d{2}, \d{2}:\d{2} - ([^:]+):', line)
                if sender:
                    sender = sender[0]
                    attendance[sender] += 1
            
            if  re.findall(Kannada_upattern, line):
                match = re.search(Kannada_pattern, line, re.UNICODE)
                if match:
                    sender = re.findall(r'\d{2}/\d{2}/\d{2}, \d{2}:\d{2} - ([^:]+):', line)
                    if sender:
                        sender = sender[0]
                        attendance[sender] += 1
                

    return attendance, current_month

def plot_attendance(attendance, c_month):
    member_names = list(attendance.keys())
    message_counts = list(attendance.values())
   
     
    # Plot attendance
    plt.bar(member_names, message_counts)
    
    current_month = "Attendance of " + month_mapping[int(c_month)]
    # Customize plot
    plt.xlabel('LB Member')
    plt.ylabel('NoOf Days')
    plt.title(current_month)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Display the plot
    plt.show()

# Example usage
file_path = 'c:\\Users\skbasava\\Downloads\LB.txt'  # Replace with the path to your WhatsApp chat text file
attendance, month = parse_whatsapp_messages(file_path)

plot_attendance(attendance, month)
