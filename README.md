# Major Bot

## Description

Major Bot is a Python script that automates various actions on the Major platform. It handles user authentication, daily tasks, coin management, and more, using API endpoints provided by Major.

## Features

- Authenticate users and manage sessions.
- Perform daily check-ins and complete tasks.
- Manage and swipe coins.
- Spin roulette for rewards.
- Track and log actions with detailed feedback.

## Requirements

- Python 3.8 or higher

## Usage

1. Clone this repository 
```git
git clone https://github.com/Semutireng22/major.git
```
2. Open Major folder
```
cd major
```
3. Install requirements.txt
```bash
pip install -r requirements.txt
```
4. Edit `token.txt` with your own token ([How to find token](#how-to-obtain-your-token))
5. Run script
```bash
python major.py
```

6. The script will process each account, perform actions, and print results to the console.

## How to Obtain Your Token

To run the script, you'll need to get a token from the Major bot. Follow these steps to obtain your token:

1. **Login to Telegram Web**:
   - Open [web.telegram.org](https://web.telegram.org) in the Kiwi browser.

2. **Open Major Bot**:
   - Find and open the chat with the Major bot in Telegram.

3. **Access Developer Tools**:
   - Click on the three dots in the top right corner of the Major bot chat.
   - Select **"Developer Tools"** from the menu that appears.

4. **Open the Application Tab**:
   - In Developer Tools, go to the **"Application"** tab.

5. **Find Session Storage**:
   - In the left-hand panel, locate and click on **"Session Storage"**.
   - Choose the URL that includes `major`.

6. **Locate `query_id`**:
   - Look for an entry containing `query_id`.
   - Copy the value of `query_id`

7. **Save the Token**:
   - Paste the `query_id` value into a file named `token.txt`.
   - Save the file as `token.txt`.
