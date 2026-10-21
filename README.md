# automaticqa-bday-form
Simple automatic QA testing on Bday RSVP Form
<img width="400" height="274" alt="Screen-Recording-2026-10-21-2233 (1)" src="https://github.com/user-attachments/assets/8ac1a2a1-a97e-4b89-a0a8-05308d095361" />


# Test Plan
Input test users into the appropriate text boxes, input 3 hard-coded data into g-form back-to-back til the end of data.

# Technicalities
- Selenium WebDriver for browser automation support
- ChromeDriver 156 for bridging module
- Python is the language used
- Chrome DevTools for manually scanning the elements

```mermaid
flowchart TD
    %% Start Script
    Start([Start Script Execution]) --> ValidateUsers{Check User Data Count == 3?}
    
    %% User Data Validation
    ValidateUsers -- No --> RaiseCountError[Raise ValueError: Exactly 3 users required]
    RaiseCountError --> EndScript([Terminate Script])
    
    ValidateUsers -- Yes --> CheckFields{Are all required fields present for all users?}
    CheckFields -- Missing Fields --> RaiseFieldError[Raise ValueError: Missing User Fields]
    RaiseFieldError --> EndScript

    %% Browser Setup
    CheckFields -- All Valid --> InitDriver[Initialize ChromeDriver & WebDriverWait]
    InitDriver --> LoopStart[Loop: Iterate over each User 1 to 3]

    %% Main Automation Steps
    subgraph User Automation Loop
        LoopStart --> OpenForm[Navigate to FORM_URL]
        
        %% Text Fields Input
        OpenForm --> InputName[Locate & Fill Name Textarea]
        InputName --> InputSocial[Locate & Fill IG/twt Account Textarea]
        InputSocial --> InputPhone[Locate & Fill Phone Number Textarea]
        
        %% Radio & Submit
        InputPhone --> SelectRadio[Locate & Click Overnight Radio Button: 'Yes']
        SelectRadio --> ClickSubmit[Click Submit Button: 'Kirim']
        ClickSubmit --> WaitStale[Wait for Submit Button Staleness / Navigation]
        WaitStale --> LogSuccess[Print: 'Submitted response X of 3 for User']
    end

    %% Loop Evaluation
    LogSuccess --> MoreUsers{More Users Left?}
    MoreUsers -- Yes --> LoopStart
    
    %% Cleanup & Exit
    MoreUsers -- No --> QuitDriver[driver.quit: Close Browser]
    QuitDriver --> Finish([Script Execution Complete])

    %% Error Handling Fallback
    OpenForm -. Any Runtime Error .-> QuitDriver
    InputName -. Any Runtime Error .-> QuitDriver
    SelectRadio -. Any Runtime Error .-> QuitDriver
    ClickSubmit -. Any Runtime Error .-> QuitDriver
