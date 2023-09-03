# Django_TimeTracker_2023

A time tracking app is an essential time management tool that can help you and your team become more organized, efficient, and get more things done. Simply put, a time tracking app will save you and your company precious time - and money. Time tracking app will generate almost all the reports that make organizations men power in most productive.

Main goal of the application is to complete the project / product in time or before time , track the team / developer who needs more help / low productive.

### Users:-

project manager, developer

Project manager can add projects in time tracking app , they can create multiple modules and task in projects. All task - modules are assigned by project manager to developer. Developer needs to perform all the task and submit once they are done with the task Time tracing will track the time taken by the developer to complete that task. Project Manager is the main user who need time tracking more over the other users. Project manager can generate reports project wise , they have the various charts that indicates time line and critical dead line with projects.


### Functionality Added:-

1) Welcome Mail to the user who register for the first time.
2) Page Restriction is added.
3) Plotly Charts are added to visualize the data in more enhance way.
4) If developer didn't completed the given tasks or modules then the remainder mail will be sent to him\her if last three days are remaining for the completion.
5) Meetings can be arranged by the project manager and automatic Mail will be sent to invited users/developers.
6) Report Generation is added in the project which shows monthly report of total project,modules and tasks in the tabular form. And also overall total number of projects,tasks and modules in the modular form.
7) If developer find any difficulty in the project or tasks or in any other issue they can contact to manager directly by filling up the developer submission form. Which will be directly mailed to the project manager.

### Installation
Install python on the system and Create a virtual environment.
Install the requirements.txt file using the terminal. Just copy and paste this line.
```python
pip install -r requirements.txt
```
After installing all the required libraries just add the emailid and password at the last lines of settings.py page for sending the emails during the signup and deadline and then do migration.
```python
python manage.py makemigrations
python manage.py migrate
```

## Overview of my project.

First Page
![first-page](https://user-images.githubusercontent.com/90546286/229265605-6b7df75e-e4fe-4535-841d-17ecbc2eabe5.png)
Register Page
![register-page](https://user-images.githubusercontent.com/90546286/229265604-9b614130-362d-4ad0-9437-3a671296f425.jpeg)
Login Page
![login-page](https://user-images.githubusercontent.com/90546286/229265603-74adf226-5ce2-4e9a-89d9-e25576ab4595.png)
Manager Page
![manager-page](https://user-images.githubusercontent.com/90546286/235291609-7cc5be65-afa8-42d6-9ef8-3d895a5e6960.jpeg)
Developer Page
![developer-page](https://user-images.githubusercontent.com/90546286/235291668-b917fba3-181e-43f6-a9b3-3ee8a6e4f0df.jpeg)
User Profile Page
![userprofilepage](https://user-images.githubusercontent.com/90546286/230821281-ed1dde2d-1784-4d17-aa0c-64da7ae21c56.jpeg)
Project List
![project-list](https://user-images.githubusercontent.com/90546286/229265607-5f144abf-e4c0-4e74-9212-b9299de57513.jpeg)

**(Note: This project was made as a final-year project for the Internship at Arth Infosoft Pvt. Ltd.)**
