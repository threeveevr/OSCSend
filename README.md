# OSCSend


Q: What is this?

A: This is a tool that can resend recorded OSC messages captured from VRCFT. It does not support recording yet, but does include pre-made captures

Q: Neat, what does that mean?

A: This tool emulates the data coming from a face tracked headset into a face tracking avatar without needing face tracking hardware. All you need is Unity, this tool, and an avatar that supports face tracking. The output resembles natural input from a face tracking headset.

Q: Great! How do I use it?

A: Super easy!

1: Get yourself a face tracked avatar and set up your Unity project
2: Install AV3 emulator from VCC
3: In Unity go to Tools > Avatars 3.0 Emulator > OSC Control panel > and make sure "open socket" is enabled
4: Go into play mode, click the avatar prefab in your hierarchy, then in the inspector enable mouth and eye tracking in the VRCFT menua
5: Open OSCSend
6: Click "browse" on one of the headset presets. There are headset samples included in the "Headsets" folder
7: Press Send

At this point you should see your avatars face moving! These movements are identical to someone actually wearing a Quest Pro and moving their face

The "Loop" option can be enabled to loop the messages for rapid iterating of blendshapes

This was inspired by Kadachii's app "OSC Replay" - https://github.com/KadachiiVR/osc_replay


Full disclaimer: Parts of this tool were developed with an LLM to assist with code. I am not a programmer and this program was something I originally made for my own use. I have no plans to profit off this software and only wish for it to assist others. If you would like to recreate this in its entirety without the use of AI, you have my blessing. 
