import matplotlib.pyplot as plt
import numpy as np

################################################################################

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

################################################################################

class Prime:
    def __init__(self, n=1):
        self.n = n
        self.prime = self.check_if_prime(self.n)
        self._coord = Point(0, 0)

    def check_if_prime(self, n):
        if n > 1:
            for i in range(2, n // 2):
                if n % i == 0:
                    return False
            return True

    def get_coord(self):
        return self._coord

    def set_coord(self, new_point):
        self._coord = new_point

    coord = property(get_coord, set_coord)

################################################################################

class Ulam:
    def __init__(self, n):
        # n must be odd
        self.n = n
        self.array = [[Prime() for i in range(n)] for j in range(n)]
        self.generate_array(n)
        self.add_coord_to_primes()
        self.coord_x = []
        self.coord_y = []
        self.store_coords()


    def generate_array(self, n):
        mid = self.n // 2
        self.array[mid][mid] = Prime(1)

        radius = 1
        current_number = 2

        start = Point(mid, mid)

        print(mid)

        while True:
            corners = {}
            corners["TL"] = Point((mid - radius), (mid - radius))
            corners["BL"] = Point((mid - radius), (mid + radius))
            corners["TR"] = Point((mid + radius), (mid - radius))
            corners["BR"] = Point((mid + radius), (mid + radius))


            # Go North
            # print(corners["MID"].y, corners["TR"].y)
            # 1, 0
            for i in range(start.y, corners["TR"].y, -1):
                self.array[i][mid+radius] = Prime(current_number)
                current_number += 1

            # Go West
            print(corners["TR"].x, corners["TL"].x)
            for i in range(corners["TR"].x, corners["TL"].x, -1):
                self.array[corners["TR"].y][i] = Prime(current_number)
                current_number += 1

            # Go South
            for i in range(corners["TL"].y, corners["BL"].y):
                self.array[i][corners["TL"].x] = Prime(current_number)
                current_number += 1

            # Go East + 1
            for i in range(corners["BL"].x, corners["BR"].x+1):
                self.array[corners["BL"].y][i] = Prime(current_number)
                current_number += 1
                start = Point(i, (corners["BL"].y))

                if current_number >= (n * n):
                    self.array[n-1][n-1] = Prime(n * n)
                    return self.array

            radius += 1

        return self.array


    def add_coord_to_primes(self):
        for y in range(self.n):
            for x in range(self.n):
                print(f"self.array[y][x]: {self.array[y][x]}")
                self.array[y][x].coord = self.ulam_to_coords(x, y)
                print(f"self.array[y][x]._coord.x: {self.array[y][x]._coord.x}")


    def ulam_to_coords(self, x, y):
        mid = Point(self.n // 2, self.n // 2)
        delta_x = x - mid.x
        delta_y = mid.y - y
        return Point(delta_x, delta_y)

    def store_coords(self):
        for column in range(self.n):
            for row in range(self.n):
                if self.array[column][row].prime:
                    print(str(self.array[column][row].n) + " is prime")
                    self.coord_x.append(self.array[column][row].coord.x)
                    self.coord_y.append(self.array[column][row].coord.y)

################################################################################

if __name__ == "__main__":
    n = input("Please insert an odd number: ")
    ulam = Ulam(int(n))

    print(ulam.coord_x)
    print(ulam.coord_y)

    plt.grid()
    plt.scatter(ulam.coord_x, ulam.coord_y)
    plt.show()
