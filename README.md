
# Totalticketing Test Task

**Test Task for Totalticketing**


## Problem

##### An API is used to perform operations on many items in a loop, that has 2 potential problems:
 - The request takes a long time to complete, so the user may suspect the operation has failed, and may retry, running multiple parallel jobs.

 - Due to web server request time out of 60 seconds, the user will not get their response. It is not possible to extend the timeout beyond 60 seconds.


##### Advise how we can resolve these issues:
 - Protect the server against the user submitting parallel requests, both on the server side, but also to provide the user with partial progress updates so they will get immediate and regular feedback that the task is progressing, increasing user confidence in the operation.

 - Ensure that the operation will continue and complete beyond the web server 60 seconds timeout.




## Solution

### 1. Preventing Parallel Requests:

- **Backend Protection:** The server prevents multiple parallel requests from the same user for the same task.

- **User Feedback:** Regular progress updates are provided to users through WebSocket, increasing their confidence that the operation is progressing.

### 2. Handling Web Server Timeout:

- **Background Processing:** Celery handles the long-running task in the background, ensuring it continues beyond the web server's 60-second timeout.


## Implementation Details

### 1. Task Processing with Celery:

- **Celery:** Used for processing background tasks to avoid server timeout issues. Tasks are executed asynchronously, allowing the web server to respond quickly.

- **Redis:** Acts as the message broker for Celery, managing task queues and results.

### 2. Real-Time Updates with WebSocket:

- **Channels (Daphne):** Utilized for WebSocket communication, providing real-time updates to the client about task progress.

- **Client-Side Handling:** The client interface disables the button upon task initiation and re-enables it only when the task is completed.

### 3.  Task Management:

- **Task Status Check:** On page load, an API endpoint verifies if a task is in progress for the user. If a task is found and not yet completed, the button remains disabled.

- **UserTask Model:** Keeps track of the status of tasks in the backend. The button's state is controlled based on the task's completion status. Once the task is completed the status gets updated in the model.

## Tech Stack
**Backend:** Django/Python

**Database:** Postgresql

**Frontend:** Django Templates, JavaScript, JQuery

**Libraries:**
- redis
- channels[daphne]
- channels-redis
- socket.io

**Services:**
- Celery
- Redis
- Flower

**Tools:**
- Docker


## Instruction to Start

Start Server
```
docker-compose up --build

```

Create a user
```
docker-compose exec -it app python manage.py createsuperuser --username=admin --email=admin@admin.com

```
## Usage

1. **Starting a Task:**
   - Users initiate the task by clicking the button, which then becomes disabled.
   - A background task is created and processed by Celery.

2. **Progress Updates:**
   - The client receives real-time progress updates through WebSocket.
   - The button remains disabled until the task is marked as complete.

3. **Task Status Verification:**
   - On page load, the application checks if there is an ongoing task for the user.
   - The button's state is updated based on the task's status in the UserTask model.
## Alternate Solution (Using Polling)

#### Django Task Processing with Celery and Polling

## Solution

To address these issues, the following approach can be implemented:

1. **Preventing Parallel Requests:**
   - **Backend Management:** The server ensures that multiple parallel requests for the same task from the same user are not processed.
   - **User Feedback:** Regular status updates are provided through polling, enhancing user confidence that the task is progressing.

2. **Handling Web Server Timeout:**
   - **Background Processing:** Celery processes long-running tasks in the background, allowing them to continue beyond the web server's 60-second timeout.
