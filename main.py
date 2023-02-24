from error import enter_press
from optimizer import run
import multiprocessing


if __name__ == '__main__':
    error_handler = multiprocessing.Process(target=enter_press)
    runner = multiprocessing.Process(target=run)

    runner.start()

    
    error_handler.start()

    runner.join()
    if not runner.is_alive():
        error_handler.terminate()