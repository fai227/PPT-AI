import numpy as np
import constants

class board_detector:
    previous_next_array = np.zeros(1)

    def check_next_turn(screenshot_array) -> bool:
        next_array = screenshot_array[55:73, 379:399]
        data_length = np.prod(next_array.shape)
        similarity = board_detector.get_similarity(board_detector.previous_next_array, next_array, data_length)
        
        if similarity < constants.NEXT_SIMILARITY_THRESHOLD:
            board_detector.previous_next_array = next_array
            return True
        
        board_detector.previous_next_array = next_array
        return False

    def get_board(screenshot_array):
        board = []
        return 

    
    def get_similarity(a, b, data_length):
        return np.count_nonzero(np.isclose(a=a, b=b, atol=20)) / data_length
