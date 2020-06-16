# Decode Sortahand Gesture on a virtual keyborad using the SHARK2(ShortHand Aided Rapid Keyboarding) algorithm

Given a dictionary containing 10000 words, implementation of SHARK2 algorithm (as in research paper: http://pokristensson.com/pubs/KristenssonZhaiUIST2004.pdf) to decode a user input gesture and output the best decoded word.

<img src = "shark.png" width = "500">

## Functions for implementation:
    1.Sampling
    2.Pruning
    3.Shape Channel
    4.Location Channel
    5.Integration

### Sampling

SHARK2 actually compares the user input pattern with standard templates for each word. When we compare different patterns, it is important to make them comparable. No matter how long or how short the gesture is, we uniformly sample 100 points along the pattern.
 
### Pruning

Start-to-start and end-to-end distances between each template and the unknown gesture is calculated. The two patterns should be normalized in scale and translation. Normalization is achieved by scaling the largest side of the bounding box to a parameter L.

**s = L/max(W,H)**

### Shape Channel
Relative coordinate, normalized
<img src = "shape_channel.png" width = "250">

### Location Channel
Absolute coordinate, unnormalized
<img src = "location_channel.png" width = "250">
   
#### Integration score = a * shape score + b * location score where a and b are parameters and a + b = 1
   
### Get Best Word

Select top-N, say, top-3 words with highest integration scores. Multiply with their corresponding probabilities.
_For example, integration_score(“too”) == integration_score(“to”), since prob(“too”) < prob(“to”), integration_score(“too”) * prob(“too”) < integration_score(“to”) * prob(“to”). Hence we choose word “to” and algorithm terminated._
 

 
