KNOWN ISSUE: Currently, if you click "Stop Main" while there is a rate sleep, the rate sleep will restart unless you close out Script Dock entirely. If you stop during normal operation there are no issues.

Oversight: MAXLENGTH is actually MINLENGTH (Minimum instead of maximum) Will fix soon

# RE-FLEX

Prerequisites:

Copy and paste into terminal:

pip install requests pyaes pbkdf2 yagmail

Then press enter.

.
Disclaimer: This is spoofing the Android App, you should be able to use it still if you use iPhone, but when you set the version you are following the Android Version number
.
WARNING!: Never copy the userdata folder to another device. If you need to use a different device, have a fresh script with a blank userdata folder and do the sign in process on that device. The challenge link itself can be done anywhere as long as the maplanding is pasted into the script terminal
.

Everything is done from Script_Dock.py

First time setup:

Set_App_Version:

Just put the Android Flex app version here and click save

Set_User_Agent:

Select from the list and click set, or click random. Once set, this button will not be here in the future when running script dock to prevent different user agent devices.

Start Main:

Go through the challenge link stuff, paste the maplanding url in the terminal that Script_Dock opened with(you will see the request for the URL) and once you get to Scanning..., Stop Main

Choose_Station_Filter:

Select the stations you want to work at, and click Generate List, you can close this

Set_Filter_Values:

Set your filters based on whatever criteria you desire, then click save. If you have many stations the filter list will scroll.

Note: headstart is in minutes

Once done, Start Main, and then,

Check_Logs:

This will let you know if everything is working.

Yagmail uses gmail with app password, so you will need to set that up for notifications via email, it's disabled by default
