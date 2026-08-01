# Gradient Descent

# Quiz: Gradient Descent

## Question 1

How does Gradient Descent adjust model parameters?

A) By increasing the error to find better predictions  
B) By moving in the direction of the steepest gradient (negative direction of the loss function)

**Answer:** B) By moving in the direction of the steepest gradient (negative direction of the loss function)

**Explanation:** Gradient Descent adjusts parameters by taking steps proportional to the negative of the gradient, which points towards reducing error.

## Question 2

What does a large learning rate do during the optimization process?

A) It ensures convergence quickly  
B) It may lead to overshooting the minimum and cause instability

**Answer:** B) It may lead to overshooting the minimum and cause instability

**Explanation:** A large learning rate can cause the model to move far from its current position in the parameter space, potentially overshooting the minimum loss point and making it harder for convergence.

## Question 3

Why is a small learning rate not ideal during optimization?

A) It makes the optimization too slow  
B) It may take an unnecessarily long time to converge  

**Answer:** A) It makes the optimization too slow

**Explanation:** With a very small learning rate, the model takes tiny steps towards minimizing the loss function, which can make the optimization process painfully slow and inefficient.

## Question 4

In what scenario might the optimal learning rate be difficult to determine?

A) When the landscape is simple  
B) When the loss surface has multiple local minima or irregularities  

**Answer:** B) When the loss surface has multiple local minima or irregularities

**Explanation:** In complex, non-convex landscapes with many local minima or other irregular features, determining a single optimal learning rate can be challenging.

## Question 5

What does the dopamine system in neuroscience encode?

A) The difference between expected and received sensory input  
B) Rewards that reinforce desired behaviors  

**Answer:** A) The difference between expected and received sensory input

**Explanation:** In biological systems, dopamine typically encodes prediction errors—the discrepancies between what a brain predicts will happen and what actually happens. This is closely related to the concept of error correction in Gradient Descent.

## Question 6

What is backpropagation in artificial neural networks?

A) A method for propagating errors through layers from output to input  
B) A mechanism that computes gradients to adjust weights  

**Answer:** B) A mechanism that computes gradients to adjust weights

**Explanation:** Backpropagation calculates gradient values for each weight in a network, which are then used to update those weights. This allows the model to learn and improve its predictions.

## Question 7

What is an optimization path where errors are propagated backward through every layer using precise mathematical derivatives?

A) Gradient Descent  
B) Backpropagation  

**Answer:** B) Backpropagation

**Explanation:** Backpropagation, unlike gradient descent which adjusts weights based on the overall error, computes and propagates gradients through each layer to adjust weights. This is a key difference in how it operates within neural networks.

## Question 8

In what context does the brain's learning process resemble Gradient Descent?

A) Learning involves making predictions and correcting them  
B) Both involve adjusting connections based on experience  

**Answer:** A) Learning involves making predictions and correcting them

**Explanation:** The brain updates its internal models by first predicting sensory inputs, then comparing these predictions to actual outcomes. If the prediction error is large, it adjusts neural connections (weights), which parallels gradient descent's process of updating parameters in response to gradients.

## Question 9

What could be a reason for children learning from fewer examples compared to modern machine learning systems?

A) Children use more precise mathematical derivatives  
B) Biological learning processes are inherently simpler and less computationally intensive  

**Answer:** B) Biological learning processes are inherently simpler and less computationally intensive

**Explanation:** Modern AI uses sophisticated algorithms like backpropagation that require detailed calculations. Biological brains have evolved simpler, yet highly effective mechanisms for learning from experience.
