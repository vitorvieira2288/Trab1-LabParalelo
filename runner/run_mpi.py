import subprocess
import os

from file_manager import FileManager

class RunMPIPrimos:
    """
    A utility class to compile and run MPI programs using mpicc and mpirun.
    """

    __file_manager: FileManager

    def __init__(self, interest_folder: str):
        self.__file_manager = FileManager(interest_folder)
        files = self.__file_manager.list_files(ignore_extensions=[])

        for file_name in files:
            self.compile_with_mpicc(f"{interest_folder}/{file_name}")

    def compile_with_mpicc(self, file_path: str) -> None:
        """
        Compiles a MPI program using mpicc.

        Parameters:
            file_path (str): Path to the source .c file
            output (str): Name of the compiled output file (default: 'program')
        """
        if not os.path.isfile(file_path):
            raise RuntimeError(f"Error: File '{file_path}' not found.")
        
        output, extension = os.path.splitext(file_path)

        if extension != ".c":
            return

        try:
            subprocess.run(
                ['mpicc', file_path, '-o', output, "-lm"],
                capture_output=True,
                check=True  # Raises CalledProcessError on failure
            )

            print(f"File {file_path} compiled with success.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Program {file_path} does not compile.")
        except FileNotFoundError:
            raise RuntimeError("Error: 'mpicc' not found. Make sure it is "
                               "installed and available in.")
        
    def run_program(self, path, num_procs=1, args=None) -> float:
        """
        Runs a compiled MPI program using mpirun.

        Parameters:
            executable_path (str): Path to the compiled executable
            num_processes (int): Number of processes to run (default: 2)
            args (list): Optional list of arguments to pass to the executable

        Returns:
            float: The execution time of the program.
        """
        if not os.path.isfile(path):
            return f"Error: Executable '{path}' not found."

        command = ['mpirun', '-n', str(num_procs), path]
        
        if args:
            command.extend(args)

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
        

    def run_all(self, exec_number=30, num_procs=1, **kwargs) -> dict[str, float]:
        """
        Executes all available MPI programs multiple times and records execution 
        times.

        For each source file listed by the internal file manager, this method:
        - Executes the corresponding compiled MPI program `exec_number` times.
        - Collects and averages the execution time results.
        - Saves the individual times and the calculated average to a report file.

        Args:
            exec_number (int, optional): Number of times to run each executable. 
                Defaults to 30.
            num_procs (int, optional): Number of MPI processes to use in each 
                execution. Defaults to 1.
            **kwargs: Additional keyword arguments passed to the `run_program` 
                method.

        Returns:
            dict[str, float]: A dictionary that maps a file_name in his average
            execution time.

        Side Effects:
            - Creates a report file for each program in the `relatorio/` 
                directory.
            - Prints execution progress and average times to the console.
        """
        result_means = {}

        for file_name in self.__file_manager.list_files(show_path=True):
            times = []

            print(f"Executando {file_name}...\n")

            for _ in range(exec_number):
                time = self.run_program(file_name, num_procs=num_procs, **kwargs)
                times.append(time)

            mean = sum(times)/exec_number
            result_means[file_name] = mean

            content = list(map(lambda time: str(time), times))
            #Add the mean description on the bottom of the file
            content += [ f"\nA média é: {mean}" ]

            self.__file_manager.write_generator(
                f"relatorio/{file_name}/num_procs_{num_procs}.txt", content
            )

            print(f"{file_name} executado com média: {mean}.\n")

        return result_means