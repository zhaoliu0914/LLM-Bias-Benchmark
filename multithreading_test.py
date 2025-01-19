import time
import threading
import concurrent.futures


def foo(name: str) -> str:
    print(f"Thread {name} start.")
    time.sleep(2)
    print(f"Thread {name} finish.")
    return name + "0"

if __name__ == '__main__':
    print(f"Python programming Start.........")

    t1 = threading.Thread(target=foo, args=("1"))
    t1.start()

    t2 = threading.Thread(target=foo, args=("2"))
    t2.start()

    #t1.join()
    #t2.join()


    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        future3 = pool.submit(foo, ("3"))
        future4 = pool.submit(foo, ("4"))
        future5 = pool.submit(foo, ("5"))

        print(f"Result result3 = {future3.result()}")
        print(f"Result result4 = {future4.result()}")
        print(f"Result result5 = {future5.result()}")

    result_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        future6 = pool.submit(foo, ("6"))
        result_list.append(future6)
        #print(f"Result result6 = {future6.result()}")

        future7 = pool.submit(foo, ("7"))
        result_list.append(future7)
        #print(f"Result result7 = {future7.result()}")

        future8 = pool.submit(foo, ("8"))
        result_list.append(future8)
        #print(f"Result result8 = {future8.result()}")

    for future in result_list:
        print(f"Result = {future.result()}")


    print(f"Python programming End.........")

