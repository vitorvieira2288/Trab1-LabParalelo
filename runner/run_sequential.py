import subprocess
import os

from file_manager import FileManager

class RunSequential:
    """
    A utility class to compile and run the sequential version.
    """

    __path: str

    def __init__(self, path: str):
        self.__path = path
        self.compile()

    def compile(self) -> None:
        """
        Compiles a C program using gcc.
        """
        if not os.path.isfile(self.__path):
            raise RuntimeError(f"Error: File '{self.__path}' not found.")
        
        output, extension = os.path.splitext(self.__path)

        if extension != ".c":
            return

        try:
            subprocess.run(
                ['gcc', self.__path, '-o', output, "-lm"],
                capture_output=True,
                check=True  # Raises CalledProcessError on failure
            )

            self.__path = output

            print(f"File {self.__path} compiled with success.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Program {self.__path} does not compile.")
        except FileNotFoundError:
            raise RuntimeError("Error: 'mpicc' not found. Make sure it is "
                               "installed and available in.")
        
    def run_program(self, args=None) -> float:
        """
        Runs a compiled C program.

        Parameters:
            args (list): Optional list of arguments to pass to the executable

        Returns:
            float: The execution time of the program.
        """
        if not os.path.isfile(self.__path):
            return f"Error: Executable '{self.__path}' not found."

        command = [self.__path]
        
        if args:
            command.extend(str(arg) for arg in args)

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            _, exec_time_text, _ = result.stdout.split("\n")
            _, time_value = exec_time_text.split(": ")
            
            return float(time_value)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Execution error:\n{e.stderr}")
        except FileNotFoundError:
            raise RuntimeError("Error: 'mpirun' not found. Make sure MPI is "
                               "installed and available in the system PATH.")

    def get_mean(self, n_times: int, **kwargs) -> float:
        """
        Execute the program `n_times` times, and returns the average execution
        time.

        Args:
            n_times (int): The number of executions to be applied.
            *kwargs: the program args.

        Returns:
            float: the average execution time.

        Side Effects:
            Writes all times and the mean in a file.
        """
        executions = []

        for _ in range(n_times):
            time = self.run_program(**kwargs)
            executions.append(time)

        mean = sum(executions) / n_times

        content = list(map(lambda time: str(time), executions))
        content += [f"\nO tempo médio foi: {mean}"]

        fm = FileManager("sequential")
        fm.write_generator("relatorio/sequential/primos.txt", content)
        return mean

if __name__ == "__main__":
    run = RunSequential("./sequential/primos.c")
    mean = run.get_mean(n_times=30, args=["1000000"])
    print(mean)
