# Decode_Gesture_SHARK2_algo
Given a dictionary containing 10000 words, implementation of SHARK2 algorithm (as in research paper: http://pokristensson.com/pubs/KristenssonZhaiUIST2004.pdf) to decode a user input gesture and output the best decoded word.

<img src = "shark.png" width = "500">

## Functions:
    Sampling
    Pruning
    Shape Channel
    Location Channel
    Integration

 Sampling
 SHARK2 actually is doing camparations between user input pattern with standard templates of each word.
When we compare different patterns, it is important to make them comparable.
No matter how long or how short the gesture is, we uniformly sample 100 points along the pattern.


 
 Pruning
 Compute start-to-start and end-to-end distances between a template and the unknown gesture.
Note that the two patterns are all normalized in scale and translation.
Normalization is achieved by scaling the largest side of the bounding box to a parameter L.
s = L/max(W,H)

 Shape Channel
 Relative coordinate, normalized
 <img src = "shape_channel.png" width = "500">
 
  Location Channel
  Absolute coordinate, unnormalized
 <img src = "location_channel.png" width = "500">
 
  
  
  Integration score = a * shape score + b * location score where a and b are parameters and a + b = 1
   Get Best Word
Select top-N, say, top-3 words with highest integration scores. Multiply with their corresponding probabilities.
For example, integration_score(“too”) == integration_score(“to”), since prob(“too”) < prob(“to”), integration_score(“too”) * prob(“too”) < integration_score(“to”) * prob(“to”)
Hence we choose word “to” and algorithm terminated.
 

 
