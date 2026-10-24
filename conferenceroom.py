import tkinter as tk
from tkinter import ttk, messagebox


# ==========================
# STUDENT CLASS
# ==========================
class Student:
    def __init__(self, student_number, name, password):
        self.student_number = student_number
        self.name = name
        self.password = password
        self.email = f"{student_number}@edu.vut.ac.za"

    def __str__(self):
        return f"{self.name} ({self.student_number})"


# ==========================
# ROOM CLASS
# ==========================
class ConferenceRoom:
    def __init__(self, room_number, capacity):
        self.room_number = room_number
        self.capacity = capacity
        self.status = "Available"

    def book_room(self):
        self.status = "Booked"


# ==========================
# BOOKING CLASS
# ==========================
class Booking:
    def __init__(self, organizer, room):
        self.organizer = organizer
        self.room = room
        self.members = []
        self.confirmations = {}

    def add_member(self, student):
        self.members.append(student)
        self.confirmations[student.student_number] = False

    def send_invitations(self):
        invitations = []

        for member in self.members:
            invitations.append(
                f"Invitation sent to {member.email}"
            )

        return "\n".join(invitations)

    def confirm_member(self, student_number):
        if student_number in self.confirmations:
            self.confirmations[student_number] = True

    def all_confirmed(self):
        return all(self.confirmations.values())


# ==========================
# SAMPLE STUDENTS
# ==========================
students = [
    Student("224703367", "Siamang Khoza", "1235"),
    Student("224703368", "Neo", "123456"),
    Student("224703369", "Katlego", "1234567"),
    Student("224703370", "Mpho", "12345678")
]

# ==========================
# ROOMS
# ==========================
rooms = [
    ConferenceRoom("CR101", 5),
    ConferenceRoom("CR102", 10),
    ConferenceRoom("CR103", 10),
    ConferenceRoom("CR104", 15),
    ConferenceRoom("CR105", 15)
]

current_booking = None

# ==========================
# MAIN WINDOW
# ==========================
root = tk.Tk()
root.title("Conference Room Booking System")
root.geometry("700x600")
root.resizable(False, False)

# ==========================
# LOGIN FRAME
# ==========================
login_frame = tk.Frame(root)
login_frame.pack(fill="both", expand=True)

tk.Label(
    login_frame,
    text="Conference Room Booking System",
    font=("Arial", 18, "bold")
).pack(pady=20)

tk.Label(login_frame, text="Student Number").pack()

student_no_entry = tk.Entry(login_frame)
student_no_entry.pack()

tk.Label(login_frame, text="Student Name").pack()

student_name_entry = tk.Entry(login_frame)
student_name_entry.pack()

tk.Label(login_frame, text="Password").pack()

password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()


# ==========================
# DASHBOARD
# ==========================
dashboard_frame = tk.Frame(root)

room_var = tk.StringVar()

member_vars = {}


def show_dashboard():
    login_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)


def login():
    global organizer

    student_number = student_no_entry.get()
    student_name = student_name_entry.get()
    password = password_entry.get()

    if student_number and student_name and password:

        organizer = Student(
            student_number,
            student_name,
            password
        )

        show_dashboard()

    else:
        messagebox.showerror(
            "Error",
            "Fill all fields"
        )


tk.Button(
    login_frame,
    text="Login",
    command=login
).pack(pady=20)

# ==================================
# DASHBOARD CONTENTS
# ==================================

title = tk.Label(
    dashboard_frame,
    text="Conference Room Booking",
    font=("Arial", 16, "bold")
)

title.pack(pady=10)

# ROOM SELECTION
tk.Label(
    dashboard_frame,
    text="Select Conference Room:"
).pack()

room_combo = ttk.Combobox(
    dashboard_frame,
    textvariable=room_var
)

room_combo["values"] = [
    f"{room.room_number} "
    f"(Capacity {room.capacity})"
    for room in rooms
]

room_combo.pack(pady=5)

# MEMBER SELECTION
tk.Label(
    dashboard_frame,
    text="Select Members:"
).pack(pady=10)

member_frame = tk.Frame(dashboard_frame)
member_frame.pack()

for student in students:
    var = tk.IntVar()

    chk = tk.Checkbutton(
        member_frame,
        text=f"{student.name} ({student.student_number})",
        variable=var
    )

    chk.pack(anchor="w")

    member_vars[student.student_number] = var

status_text = tk.Text(
    dashboard_frame,
    width=65,
    height=10
)

status_text.pack(pady=15)


# ==================================
# SEND INVITATIONS
# ==================================
def book_room():

    global current_booking

    room_selected = room_combo.current()

    if room_selected == -1:
        messagebox.showerror(
            "Error",
            "Select a room"
        )
        return

    room = rooms[room_selected]

    current_booking = Booking(
        organizer,
        room
    )

    selected_count = 0

    for student in students:

        if member_vars[
                student.student_number].get() == 1:

            current_booking.add_member(student)
            selected_count += 1

    if selected_count == 0:

        messagebox.showerror(
            "Error",
            "Select at least one member"
        )

        return

    emails = current_booking.send_invitations()

    status_text.delete(1.0, tk.END)
    status_text.insert(tk.END, emails)

    messagebox.showinfo(
        "Emails Sent",
        "Invitations have been sent."
    )


# ==================================
# CONFIRM MEMBERS
# ==================================
def confirm_all():

    if current_booking is None:
        return

    for member in current_booking.members:
        current_booking.confirm_member(
            member.student_number
        )

    status_text.insert(
        tk.END,
        "\n\nAll members confirmed."
    )


# ==================================
# FINALIZE BOOKING
# ==================================
def finalize_booking():

    if current_booking is None:
        return

    if current_booking.all_confirmed():

        current_booking.room.book_room()

        messagebox.showinfo(
            "Success",
            f"{current_booking.room.room_number} "
            f"booked successfully!"
        )

        status_text.insert(
            tk.END,
            f"\n\nRoom Status: "
            f"{current_booking.room.status}"
        )

    else:

        messagebox.showwarning(
            "Pending",
            "Waiting for confirmations."
        )


tk.Button(
    dashboard_frame,
    text="Send Invitations",
    command=book_room
).pack(pady=5)

tk.Button(
    dashboard_frame,
    text="Confirm Members",
    command=confirm_all
).pack(pady=5)

tk.Button(
    dashboard_frame,
    text="Finalize Booking",
    command=finalize_booking
).pack(pady=5)

root.mainloop()