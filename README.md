# LookAhead
Hack The North X Submission - visual impairment aid using eye tracking 

## inspiration
After recently learning that most blind people still retain a limited level of sight, we immediately set out to create a tool that could help them.
Many blind people are able to see very faint shapes, and a similarity can be drawn between their level of sight and a highly overexposed photo.

## functionality
Our tool provides two main functionalities: object identification and obstacle detection.
LookAhead is built using the AdHawk MindLink glasses, which allow us to easily see and analyze images from the wearer's point of view, as well as track where the wearer is looking at the moment.
We pride ourselves on our fully voice-controlled software, making it easily usable by the visually impaired.

### object identification
Object identification was the first and most complicated function to implement. It consists of five steps:
1. speech activation
2. live video recording from the AdHawk MindLink glasses
3. live google cloud API requests to identify objects within the frame
4. live eye tracking to see which object the wearer is looking at
5. text to speech broadcasting the object that the wearer is looking at
It is there to help the visually impaired who have a faint idea that something is there, but are unable to see details beyond partial edges or similar.

### obstacle detection
Obstacle detection warns the wearer of any impending obstacle that they may trip on or bump into by giving audio cues.
It narrows down the most impending obstacle by weighting the size of the obstacle as well as it's proximity to the wearer's predicted path of travel.
