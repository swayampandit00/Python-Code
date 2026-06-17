import pandas as pd
from datetime import datetime
import os

class AttendanceManager:
    def __init__(self, attendance_file='attendance.csv'):
        self.attendance_file = attendance_file
        self.initialize_attendance_file()
    
    def initialize_attendance_file(self):
        """Create attendance file if it doesn't exist"""
        if not os.path.exists(self.attendance_file):
            df = pd.DataFrame(columns=['Name', 'Date', 'Time', 'Status'])
            df.to_csv(self.attendance_file, index=False)
            print(f"Created {self.attendance_file}")
    
    def add_attendance(self, name, status='Present'):
        """Add attendance record for a person"""
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        
        df = pd.read_csv(self.attendance_file)
        
        # Check if person already marked attendance today
        today_attendance = df[(df['Name'] == name) & (df['Date'] == date)]
        
        if today_attendance.empty:
            new_entry = pd.DataFrame([[name, date, time, status]], 
                                    columns=['Name', 'Date', 'Time', 'Status'])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(self.attendance_file, index=False)
            return True
        return False
    
    def get_attendance_by_date(self, date):
        """Get attendance records for a specific date"""
        df = pd.read_csv(self.attendance_file)
        return df[df['Date'] == date]
    
    def get_attendance_by_person(self, name):
        """Get all attendance records for a specific person"""
        df = pd.read_csv(self.attendance_file)
        return df[df['Name'] == name]
    
    def get_all_attendance(self):
        """Get all attendance records"""
        return pd.read_csv(self.attendance_file)
    
    def generate_report(self, start_date=None, end_date=None):
        """Generate attendance report for a date range"""
        df = pd.read_csv(self.attendance_file)
        
        if start_date:
            df = df[df['Date'] >= start_date]
        if end_date:
            df = df[df['Date'] <= end_date]
        
        # Calculate attendance statistics
        total_records = len(df)
        unique_persons = df['Name'].nunique()
        
        print(f"\n=== Attendance Report ===")
        print(f"Date Range: {start_date} to {end_date}")
        print(f"Total Records: {total_records}")
        print(f"Unique Persons: {unique_persons}")
        print(f"\nAttendance by Person:")
        
        person_stats = df.groupby('Name').size().reset_index(name='Days Present')
        print(person_stats.to_string(index=False))
        
        return df
    
    def export_to_excel(self, output_file='attendance_report.xlsx'):
        """Export attendance data to Excel file"""
        df = pd.read_csv(self.attendance_file)
        df.to_excel(output_file, index=False)
        print(f"Attendance data exported to {output_file}")

if __name__ == "__main__":
    manager = AttendanceManager()
    
    print("Attendance Manager")
    print("1. View all attendance")
    print("2. View attendance by date")
    print("3. View attendance by person")
    print("4. Generate report")
    print("5. Export to Excel")
    
    choice = input("Enter your choice (1-5): ")
    
    if choice == '1':
        print(manager.get_all_attendance())
    elif choice == '2':
        date = input("Enter date (YYYY-MM-DD): ")
        print(manager.get_attendance_by_date(date))
    elif choice == '3':
        name = input("Enter person's name: ")
        print(manager.get_attendance_by_person(name))
    elif choice == '4':
        start_date = input("Enter start date (YYYY-MM-DD, leave blank for all): ")
        end_date = input("Enter end date (YYYY-MM-DD, leave blank for all): ")
        manager.generate_report(start_date if start_date else None, end_date if end_date else None)
    elif choice == '5':
        output_file = input("Enter output filename (default: attendance_report.xlsx): ")
        manager.export_to_excel(output_file if output_file else 'attendance_report.xlsx')
    else:
        print("Invalid choice")
