import sys

from run_mpi import RunMPIPrimos
from file_manager import FileManager

if __name__ == "__main__":
    if not len(sys.argv) in (2, 4):
        raise ValueError("Bad format. try:\n    "
                         "python3 runner <folder> -e <execution_number>"
                         "\n\nfolder: can be naive or bag of tasks\n"
                         "execution_number: is the number of times that a single"
                         " program will be executed."
                         "\n\nNote: The use of -e flag is optional, and the "
                         "default value is 30")
    
    folder = sys.argv[1]
    exec_number = 30

    if len(sys.argv) == 4:
        exec_number = int(sys.argv[3])

    run_primos = RunMPIPrimos(folder)
    file_manager = FileManager(folder)

    #Execute with 1, 2 and 4 processes
    r1 = run_primos.run_all(num_procs=1, exec_number=exec_number, args=['1000000'])
    r2 = run_primos.run_all(num_procs=2, exec_number=exec_number, args=['1000000'])
    r4 = run_primos.run_all(num_procs=4, exec_number=exec_number, args=['1000000'])

    print(r1, r2, r4)

    names = file_manager.list_files(show_path=True)
    for name in names:
        speed_up_2_procs = r1[name] / r2[name]
        efficiency_2_procs  =speed_up_2_procs/2

        speed_up_4_procs = r1[name] / r4[name]
        efficiency_4_procs  =speed_up_4_procs/2

        content = [
            f"Speed-Up com 2 processos: {speed_up_2_procs}",
            f"Eficiência com 2 processos: {efficiency_2_procs}\n"
            f"Speed-Up com 4 processos: {speed_up_4_procs}",
            f"Eficiência com 4 processos: {efficiency_4_procs}",
        ]

        file_manager.write_generator(f"relatorio/{name}/avaliacao.txt", content)