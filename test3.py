import mysql.connector


conn = mysql.connector.connect(host='localhost', user='root', password='12345', database='test_db6')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    StudentName VARCHAR(30),
    CollegeName VARCHAR(50),
    Round1Marks FLOAT CHECK (Round1Marks BETWEEN 0 AND 10),
    Round2Marks FLOAT CHECK (Round2Marks BETWEEN 0 AND 10),
    Round3Marks FLOAT CHECK (Round3Marks BETWEEN 0 AND 10),
    TechnicalRoundMarks FLOAT CHECK (TechnicalRoundMarks BETWEEN 0 AND 20),
    TotalMarks FLOAT CHECK (TotalMarks BETWEEN 0 AND 50),
    Result TEXT,
    UserRank INT
)
''')
conn.commit()


def validate_input(prompt, max_length):
    while True:
        value = input(prompt).strip()
        if value == '':
            return print("Enter the name again as it is blank")
        if len(value) <= max_length:
            return value
        else:
            print(f"Error: Input exceeds {max_length} characters. Try again.")


def validate_marks(prompt, min_val, max_val):
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Error: Value should be between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")


num_users = int(input("Enter the number of candidates: "))

for i in range(num_users):
    print(f"\nEnter details for candidate {i+1}:")
    
    StudentName = validate_input("Enter student name: ", 30)
    CollegeName = validate_input("Enter college name: ", 50)
    
    Round1Marks = validate_marks("Enter Round 1 Marks (0-10): ", 0, 10)
    Round2Marks = validate_marks("Enter Round 2 Marks (0-10): ", 0, 10)
    Round3Marks = validate_marks("Enter Round 3 Marks (0-10): ", 0, 10)
    TechnicalRoundMarks = validate_marks("Enter Technical Round Marks (0-20): ", 0, 20)
    
    
    TotalMarks = Round1Marks + Round2Marks + Round3Marks + TechnicalRoundMarks
    
    
    Result = "Selected" if TotalMarks >= 35 else "Rejected"

    
    cursor.execute('''
    INSERT INTO Users (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, TotalMarks, Result) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, TotalMarks, Result))
    
    conn.commit()


cursor.execute("SELECT ID, TotalMarks FROM Users ORDER BY TotalMarks DESC, ID ASC")

rank = 1
for index, (user_id, _) in enumerate(cursor.fetchall(), start=1):
    cursor.execute("UPDATE Users SET UserRank = %s WHERE ID = %s", (rank, user_id))
    rank += 1
conn.commit()


cursor.execute("SELECT StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, TotalMarks, Result, UserRank FROM Users ORDER BY UserRank")
records = cursor.fetchall()

print("\nFinal Results:")
print("-----------------------------------------------------------------------------------")
print("Student Name | College Name | R1 Marks | R2 Marks | R3 Marks | Tech Marks | Total | Result   | Rank")
print("-----------------------------------------------------------------------------------")

for row in records:
    print(f"{row[0]:<15} | {row[1]:<15} | {row[2]:^8} | {row[3]:^8} | {row[4]:^8} | {row[5]:^10} | {row[6]:^5} | {row[7]:^8} | {row[8]:^4}")
cursor.close()
conn.close()
