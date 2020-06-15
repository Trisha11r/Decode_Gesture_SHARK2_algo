'''

You can modify the parameters, return values and data structures used in every function if it conflicts with your
coding style or you want to accelerate your code.

You can also import packages you want.

But please do not change the basic structure of this file including the function names. It is not recommended to merge
functions, otherwise it will be hard for TAs to grade your code. However, you can add helper function if necessary.

'''

from flask import Flask, request
from flask import render_template
import time
import json
import math

app = Flask(__name__)

# Centroids of 26 keys
centroids_X = [50, 205, 135, 120, 100, 155, 190, 225, 275, 260, 295, 330, 275, 240, 310, 345, 30, 135, 85, 170, 240, 170, 65, 100, 205, 65]
centroids_Y = [85, 120, 120, 85, 50, 85, 85, 85, 50, 85, 85, 85, 120, 120, 50, 50, 50, 50, 85, 50, 50, 120, 50, 120, 50, 120]

# Pre-process the dictionary and get templates of 10000 words
words, probabilities = [], {}
template_points_X, template_points_Y = [], []
file = open('words_10000.txt')
content = file.read()
file.close()
content = content.split('\n')
for line in content:  
    line = line.split('\t')
    words.append(line[0])
    probabilities[line[0]] = float(line[2])
    template_points_X.append([])
    template_points_Y.append([])
    for c in line[0]:
        template_points_X[-1].append(centroids_X[ord(c) - 97])
        template_points_Y[-1].append(centroids_Y[ord(c) - 97])


def generate_sample_points(points_X, points_Y):
    '''Generate 100 sampled points for a gesture.

    In this function, we should convert every gesture or template to a set of 100 points, such that we can compare
    the input gesture and a template computationally.

    :param points_X: A list of X-axis values of a gesture.
    :param points_Y: A list of Y-axis values of a gesture.

    :return:
        sample_points_X: A list of X-axis values of a gesture after sampling, containing 100 elements.
        sample_points_Y: A list of Y-axis values of a gesture after sampling, containing 100 elements.
    '''

    sample_points_X, sample_points_Y = [], []

    # if gesture/template already has 100 points
    if len(points_X)==100:
        return points_X, points_Y

    #if gesture/template has only one point the coordinates of the sampled 100 points would be same
    elif len(points_X)==1:
        for i in range(100):
            sample_points_X.append(points_X[0])
            sample_points_Y.append(points_Y[0])
        return sample_points_X, sample_points_Y

    #when number of points is less than 100
    elif len(points_X)<100:
        #print(points_X)
        modVal = (100-len(points_X))%(len(points_X)-1)
        for i in range(len(points_X)-1):
            if modVal!= 0:
                p= int((100-len(points_X)-modVal)/(len(points_X)-1) + 1)
                modVal-=1
            else:
                p= int((100-len(points_X)-modVal)/(len(points_X)-1))

            distX = abs(points_X[i+1]-points_X[i])/(p+1)
            #calculate slope and constant for straight line passing through (points_X[i], points_Y[i]) and (points_X[i+1], points[Y+1])
            if points_X[i]== points_X[i+1]:
                m=0
                c=0
            else:
                m= (points_Y[i+1]-points_Y[i])/(points_X[i+1]-points_X[i])
                c= (points_Y[i]*points_X[i+1] - points_X[i]*points_Y[i+1])/((points_X[i+1]-points_X[i]))

            sample_points_X.append(points_X[i])
            sample_points_Y.append(points_Y[i])
            for j in range(p):
                if points_X[i]== points_X[i+1]:
                    xVal= points_X[i]
                    distY= abs(points_Y[i+1]-points_Y[i])/(p+1)
                    if points_Y[i]<points_Y[i+1]:
                        yVal= points_Y[i]+ (j+1)*distY
                    else:
                        yVal= points_Y[i]- (j+1)*distY
                elif points_X[i]< points_X[i+1]:
                    xVal= points_X[i]+ (j+1)*distX
                    yVal= m* xVal + c
                else:
                    xVal= points_X[i]- (j+1)*distX
                    yVal= m* xVal + c
                
                sample_points_X.append(xVal)
                sample_points_Y.append(yVal)

        sample_points_X.append(points_X[i+1])
        sample_points_Y.append(points_Y[i+1])
        # print("SAMPLE POINTS X VALUES")
        #print(sample_points_X)
        # print("SAMPLE POINTS Y VALUES")
        # print(sample_points_Y)
        return sample_points_X, sample_points_Y
    
    #when number of points is greater than 100
    else:
        i=0
        sample_points_X.append(points_X[i])
        sample_points_Y.append(points_Y[i])
        modVal= len(points_X)%99
        # if modVal==0:
        #     for i in range(len(points_X)):
        #         i_new= i+ len(points_X)/99 - 1 
        #         sample_points_X.append(points_X[i_new])
        #         sample_points_Y.append(points_Y[i_new])
        #         i+=1
        # else:
        #print('gesture point size')
        #print(len(points_X))
        while i < len(points_X)-math.floor(len(points_X)/99):
            if (modVal!=0):
                #print('Bin Size')
                #print(math.floor(len(points_X)/99))
                i_new= i + math.floor(len(points_X)/99)+1
                #print('Index')
                #print(i_new)
                sample_points_X.append(points_X[i_new])
                sample_points_Y.append(points_Y[i_new])
                i= i_new
                modVal-=1
            else:
                # print('Bin Size')
                # print(math.floor(len(points_X)/99))
                i_new= i+ math.floor(len(points_X)/99)
                # print('Index')
                # print(i_new)
                sample_points_X.append(points_X[i_new])
                sample_points_Y.append(points_Y[i_new])
                i= i_new        

        sample_points_X.append(points_X[len(points_X)-1])
        sample_points_Y.append(points_Y[len(points_Y)-1])

    return sample_points_X, sample_points_Y


# Pre-sample every template
template_sample_points_X, template_sample_points_Y = [], []
for i in range(10000):
    X, Y = generate_sample_points(template_points_X[i], template_points_Y[i])
    template_sample_points_X.append(X)
    template_sample_points_Y.append(Y)


def do_pruning(gesture_points_X, gesture_points_Y, template_sample_points_X, template_sample_points_Y):
    '''Do pruning on the dictionary of 10000 words.

    In this function, we use the pruning method described in the paper (or any other method you consider it reasonable)
    to narrow down the number of valid words so that the ambiguity can be avoided to some extent.

    :param gesture_points_X: A list of X-axis values of input gesture points, which has 100 values since we have
        sampled 100 points.
    :param gesture_points_Y: A list of Y-axis values of input gesture points, which has 100 values since we have
        sampled 100 points.
    :param template_sample_points_X: 2D list, containing X-axis values of every template (10000 templates in total).
        Each of the elements is a 1D list and has the length of 100.
    :param template_sample_points_Y: 2D list, containing Y-axis values of every template (10000 templates in total).
        Each of the elements is a 1D list and has the length of 100.

    :return:
        valid_words: A list of valid words after pruning.
        valid_probabilities: The corresponding probabilities of valid_words.
        valid_template_sample_points_X: 2D list, the corresponding X-axis values of valid_words. Each of the elements
            is a 1D list and has the length of 100.
        valid_template_sample_points_Y: 2D list, the corresponding Y-axis values of valid_words. Each of the elements
            is a 1D list and has the length of 100.
    '''
    valid_words, valid_template_sample_points_X, valid_template_sample_points_Y = [], [], []
    # TODO: Set your own pruning threshold
    threshold = 25
    # TODO: Do pruning (12 points)
    last_index = len(gesture_points_X)-1
    #print(len(template_sample_points_X))
    #print(len(gesture_points_X))
    #print(template_sample_points_X[1][0])
    for i in range(len(template_sample_points_X)):
            dist_first = math.sqrt((gesture_points_X[0]-template_sample_points_X[i][0])**2 + (gesture_points_Y[0]-template_sample_points_Y[i][0])**2)
            dist_last = math.sqrt((gesture_points_X[last_index]-template_sample_points_X[i][last_index])**2 + (gesture_points_Y[last_index]-template_sample_points_Y[i][last_index])**2)
            if dist_first< threshold and dist_last< threshold:
                valid_template_sample_points_X.append(template_sample_points_X[i])
                valid_template_sample_points_Y.append(template_sample_points_Y[i])
                valid_words.append(words[i])
    #to do: valid words
    #print(len(valid_template_sample_points_X))
    #print(len(valid_template_sample_points_Y))
    #print(valid_probabilities)
    return valid_words,valid_template_sample_points_X, valid_template_sample_points_Y

def Normalise_Points(x_points, y_points):
    minValX= min(x_points)
    maxValY= min(y_points)
    maxValX= max(x_points)
    maxValY= max(y_points)

    centre_X = (minValX-maxValX)/2
    centre_Y = (maxValY-maxValY)/2

    new_xVal, new_yVal = [], []
    for i in range(len(x_points)):
        new_xVal.append(x_points[i]-centre_X)
    for i in range(len(y_points)):
        new_yVal.append(y_points[i]-centre_Y)

    w= max(new_xVal)- min(new_xVal)
    h= max(new_yVal)- min(new_yVal)

    S= 2/max(w,h)

    n_x, n_y = [], []
    for i in range(len(new_xVal)):
        n_x.append(new_xVal[i]*S)
    for i in range(len(new_yVal)):
        n_y.append(new_yVal[i]*S)
    return n_x, n_y

def get_shape_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y):
    '''Get the shape score for every valid word after pruning.

    In this function, we should compare the sampled input gesture (containing 100 points) with every single valid
    template (containing 100 points) and give each of them a shape score.

    :param gesture_sample_points_X: A list of X-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param gesture_sample_points_Y: A list of Y-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param valid_template_sample_points_X: 2D list, containing X-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.
    :param valid_template_sample_points_Y: 2D list, containing Y-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.

    :return:
        A list of shape scores.
    '''
    shape_scores = []
    # TODO: Set your own L
    L = 1
    summation_val_s = 0
    # TODO: Calculate shape scores (12 points)
    #print(gesture_sample_points_X)
    #print(len(gesture_sample_points_X[0]))
    n_valid_template_sample_points_X, n_valid_template_sample_points_Y=[], []

    normal_gesture_sample_points_X, normal_gesture_sample_points_Y= Normalise_Points(gesture_sample_points_X, gesture_sample_points_Y)

    for i in range(len(valid_template_sample_points_X)):
        #norX, norY = [], []
        norX, norY = Normalise_Points(valid_template_sample_points_X[i],valid_template_sample_points_Y[i])
        #print(len(norX))
        n_valid_template_sample_points_X.append(norX)
        n_valid_template_sample_points_Y.append(norY)
        for j in range(len(gesture_sample_points_X)):
            dist_u_t = math.sqrt((n_valid_template_sample_points_X[i][j]-normal_gesture_sample_points_X[j])**2 + (n_valid_template_sample_points_X[i][j]- normal_gesture_sample_points_Y[j])**2)
            summation_val_s += dist_u_t
        final_score = summation_val_s/len(gesture_sample_points_X)
        shape_scores.append(final_score)
    return shape_scores



def calculate_d_pq(numSample, point_p_x, point_p_y, q_x, q_y):
    diffPQ=[]
    for i in range(numSample):
        calculate_dist = math.sqrt((point_p_x-q_x[i])**2 + (point_p_y- q_y[i])**2)
        diffPQ.append(calculate_dist)
    return min(diffPQ)

def calculate_D_pq(r,p_x, p_y, q_x, q_y):
    sumVal=0    
    for i in range(len(p_x)):
       sumVal += max((calculate_d_pq(len(p_x), p_x[i], p_y[i], q_x, q_y)-r), 0)
    return sumVal

def get_location_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y):
    '''Get the location score for every valid word after pruning.

    In this function, we should compare the sampled user gesture (containing 100 points) with every single valid
    template (containing 100 points) and give each of them a location score.

    :param gesture_sample_points_X: A list of X-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param gesture_sample_points_Y: A list of Y-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param template_sample_points_X: 2D list, containing X-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.
    :param template_sample_points_Y: 2D list, containing Y-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.

    :return:
        A list of location scores.
    '''
    location_scores = []
    alpha_vals = []
    radius = 15
    # TODO: Calculate location scores (12 points)
    delta_j = -1
    loc_score= -1
    w_sides = 0.01245
    w_mid = 0.00755
    for a in range(50):
        alpha_vals.append(w_sides-a/10000)
    for b in range(50):
        alpha_vals.append(w_mid + (b+1)/10000)
    # print("Length of alpha_vals is:")
    # print(len(alpha_vals))
    # print(alpha_vals)
    for i in range(len(valid_template_sample_points_X)):
        D_u_t = calculate_D_pq(radius, gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X[i], valid_template_sample_points_Y[i])
        D_t_u = calculate_D_pq(radius, valid_template_sample_points_X[i], valid_template_sample_points_Y[i], gesture_sample_points_X, gesture_sample_points_Y)
        for j in range(len(gesture_sample_points_X)):
            
            if D_u_t==0 and D_t_u ==0:
                delta_j=0
            else:
                delta_j = math.sqrt((valid_template_sample_points_X[i][j]-gesture_sample_points_X[j])**2 + (valid_template_sample_points_Y[i][j]- gesture_sample_points_Y[j])**2)
            #alpha_j= 1
            loc_score += alpha_vals[j] *delta_j
        location_scores.append(loc_score)
    return location_scores


def get_integration_scores(shape_scores, location_scores):
    integration_scores = []
    # TODO: Set your own shape weight
    shape_coef = 0.75
    # TODO: Set your own location weight
    location_coef = 0.50
    for i in range(len(shape_scores)):
        integration_scores.append(shape_coef * shape_scores[i] + location_coef * location_scores[i])
    return integration_scores


def get_best_word(valid_words, integration_scores):
    '''Get the best word.

    In this function, you should select top-n words with the highest integration scores and then use their corresponding
    probability (stored in variable "probabilities") as weight. The word with the highest weighted integration score is
    exactly the word we want.

    :param valid_words: A list of valid words.
    :param integration_scores: A list of corresponding integration scores of valid_words.
    :return: The most probable word suggested to the user.
    '''
    best_word = []
    # TODO: Set your own range.
    n = 3
    # TODO: Get the best word (12 points)
    for i in range(n):
        max_score= max(integration_scores)
        score_index= integration_scores.index(max_score)
        best_word.append(valid_words[score_index])
        integration_scores[score_index]= -19001
        i+=1

    #best_word= valid_words[integration_scores.index(max(integration_scores))]

    return best_word


@app.route("/")
def init():
    return render_template('index.html')


@app.route('/shark2', methods=['POST'])
def shark2():   

    start_time = time.time()
    data = json.loads(request.get_data())

    gesture_points_X = []
    gesture_points_Y = []
    for i in range(len(data)):
        gesture_points_X.append(data[i]['x'])
        gesture_points_Y.append(data[i]['y'])
    #gesture_points_X = [gesture_points_X]
    #gesture_points_Y = [gesture_points_Y]


    gesture_sample_points_X, gesture_sample_points_Y = generate_sample_points(gesture_points_X, gesture_points_Y)

    # print("length of the gesture sample points is:")
    # print(len(gesture_sample_points_X), len(gesture_sample_points_Y))

    valid_words,valid_template_sample_points_X, valid_template_sample_points_Y = do_pruning(gesture_sample_points_X, gesture_sample_points_Y, template_sample_points_X, template_sample_points_Y)

    shape_scores = get_shape_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y)

    location_scores = get_location_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y)

    integration_scores = get_integration_scores(shape_scores, location_scores)

    best_word = get_best_word(valid_words, integration_scores)

    end_time = time.time()

    return '{"best_word":"' + best_word[0] + ',' + best_word[1] + ',' + best_word[2] +  '", "elapsed_time":"' + str(round((end_time - start_time) * 1000, 5)) + 'ms"}'


if __name__ == "__main__":
    app.run()
