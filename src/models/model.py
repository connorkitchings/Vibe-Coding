"""
Template for model class or training function.
"""


class BaseModel:
    """
    Base class for all models.

    Extend this class to implement specific model architectures
    and training logic.
    """

    def __init__(self):
        pass

    def train(self, data):
        """Train the model. Replace with your logic."""
        raise NotImplementedError("Implement training logic here.")
