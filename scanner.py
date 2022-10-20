#
# scanner.py
#
# Based on code for COMP 304B Assignment 3
# Updated to Python 3 in 2021
#

# trace FSA dynamics (True | False)
# __trace__ = False
__trace__ = True
__toprint__ = False
# __toprint__ = True

class CharacterStream:
    """
    A stream of characters helper class.
    """
    def __init__(self, string):
        self.string = string
        self.last_ptr = -1
        self.cur_ptr = -1

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def peek(self):
        if self.cur_ptr+1 < len(self.string):
            return self.string[self.cur_ptr+1]
        return None

    def consume(self):
        self.cur_ptr += 1

    def commit(self):
        self.last_ptr = self.cur_ptr

    def rollback(self):
        self.cur_ptr = self.last_ptr


class Scanner:
    """
    A simple Finite State Automaton simulator.
    Used for scanning an input stream.
    """
    def __init__(self, stream):
        self.set_stream(stream)
        self.current_state=None
        self.accepting_states=[]

    def set_stream(self, stream):
        self.stream = stream

    def scan(self):
        self.current_state = self.transition(self.current_state, None)

        if __trace__:
            if __toprint__:
                print("\ndefault transition --> " + self.current_state)

            while True:
                # look ahead at the next character in the input stream
                next_char = self.stream.peek()

                # stop if this is the end of the input stream
                if next_char is None: break

                if __trace__:
                    if self.current_state is not None:
                        if __toprint__:
                            print("transition", self.current_state, "-|", next_char, end=' ')

                # perform transition and its action to the appropriate new state
                next_state = self.transition(self.current_state, next_char)

                if __trace__:
                    if __toprint__:
                        if next_state is None:
                            print("")
                        else:
                            print("|->", next_state)


                # stop if a transition was not possible
                if next_state is None:
                    break
                else:
                    self.current_state = next_state
                    # perform the new state's entry action (if any)
                    self.entry(self.current_state, next_char)

                # now, actually consume the next character in the input stream
                next_char = self.stream.consume()

            if __trace__:
                if __toprint__:
                    print("")

            # now check whether to accept consumed characters
            success = self.current_state not in self.accepting_states
            if success:
                self.stream.commit()
            else:
                self.stream.rollback()
            return success


class Req5Scanner(Scanner):
    def __init__(self, stream):
        # superclass constructor
        super().__init__(stream)

        self.gate_list = 0
        self.number = 0
        self.accepting_states = ["S6"]

    def __str__(self):
        return str(self.gate_number)

    def transition(self, state, input):
        """
        Encodes transitions and actions
        """
        if state is None:
            # initialize variables
            self.gate_list = []
            self.number = 0
            # new state
            return "S1"

        elif state == "S1":
            if input =="\n":
                return "S1"
            elif input == "L":
                return "S2"
            else:
                return "S10"

        elif state == "S2":
            if input  == 'O':
                return "S3"
            elif input == 'C':
                return "S7"
            else:
                return

        elif state == "S3":
            if input == ' ':
                return "S4"
            else:
                return

        elif state == "S4":
            if '0' <= input <= '9':
                self.number = (ord(input.lower()) - ord('0'))
                self.gate_list.append(self.number)
                return "S5"
            else:
                return

        elif state == "S5":
            if self.number+1 in self.gate_list:
                return "S6"
            elif self.number-1 in self.gate_list:
                return "S6"
            elif input == "\n":
                return "S1"

        elif state == "S6":
            return

        elif state == "S7":
            if input == ' ':
                return "S8"
            else:
                return

        elif state == "S8":
            if '0' <= input <= '9':
                number = (ord(input.lower()) - ord('0'))
                if number in self.gate_list:
                    self.gate_list.remove(number)
                return "S9"
            else:
                return

        elif state == "S9":
            if input == '\n':
                return "S1"
            else:
                return
        elif state == "S10":
            if input == "\n":
                return "S1"
            else:
                return "S10"
        else:
            return None

    def entry(self, state, input):
        pass


class Req4Scanner(Scanner):
    def __init__(self, stream):
        # superclass constructor
        super().__init__(stream)

        self.ship = -1
        self.gate = -1
        self.gate_dict = {0:[], 1:[], 2:[]}
        # define accepting states
        self.accepting_states=["S13"]

    # def __str__(self):
    #     return str(self.ship)

    def transition(self, state, input):
        """
        Encodes transitions and actions
        """
        if state is None:
            # initialize variables
            self.ship = -1
            self.gate = -1
            self.gate_dict = {0:[], 1:[], 2:[]}
            # new state
            return "S1"

        elif state == "S1":
            if input =="\n":
                return "S1"
            elif input == "S":
                return "S2"
            else:
                return "S23"

        elif state == "S2":
            if input  == 'L':
                return "S3"
            elif input in ["A", "C", "P"]:
                return "S1"
            else:
                return

        elif state == "S3":
            if input == ' ':
                return "S4"
            else:
                return

        elif state == "S4":
            if '0' <= input <= '9':
                self.ship = (ord(input.lower()) - ord('0'))
                return "S5"
            else:
                return

        elif state == "S5":
            if '0' <= input <= '9':
                self.ship = self.ship * 10 + ord(input.lower()) - ord('0')
                return "S5"
            elif input == " ":
                return "S6"
            else:
                return

        elif state == "S6":
            if '0' <= input <= '9':
                gate = (ord(input.lower()) - ord('0'))
                self.gate_dict[gate].append(self.ship)
                return "S7"
            else:
                return

        elif state == "S7":
            if input == '\n':
                return "S8"
            else:
                return

        elif state == "S8":
            if input == "\n":
                return "S8"
            elif input == "P":
                return "S24"
            elif input == "L":
                return "S9"
            elif input == "S":
                return "S14"
            else:
                return

        elif state == "S9":
            if input == 'C':
                return "S10"
            elif input == "O":
                return "S24"
            else:
                return

        elif state == "S10":
            if input == " ":
                return "S11"
            else:
                return
        elif state == "S11":
            if '0' <= input <= '9':
                self.gate = (ord(input.lower()) - ord('0'))
                return "S12"
            else:
                return

        elif state == "S12":
            if len(self.gate_dict[self.gate]) != 0:
                return "S13"
            elif input == "\n":
                return "S8"
            else:
                return

        elif state == "S13":
            return

        elif state == "S14":
            if input == 'P':
                return "S15"
            elif input == "L":
                return "S3"
            elif input in ["A", "C"]:
                return "S24"
            else:
                return

        elif state == "S15":
            if input == ' ':
                return "S16"
            else:
                return

        elif state == "S16":
            if '0' <= input <= '9':
                self.ship = (ord(input.lower()) - ord('0'))
                return "S17"
            else:
                return

        elif state == "S17":
            if '0' <= input <= '9':
                self.ship = self.ship * 10 + ord(input.lower()) - ord('0')
                return "S17"
            elif input == " ":
                return "S18"
            else:
                return

        elif state == "S18":
            if input in ["A", "B", "G"]:
                return "S24"
            elif input == "L":
                return "S20"
            elif input == "P":
                return "S19"
            else:
                return

        elif state == "S19":
            if input == "O":
                return "S24"
            elif input == "I":
                # if self.ship in self.gate_dict[gate]:
                self.gate_dict[2].remove(self.ship)
                return "S22"
            else:
                return

        elif state == "S20":
            if '0' <= input <= '9':
                gate = (ord(input.lower()) - ord('0'))
                # if self.ship in self.gate_dict[gate]:
                self.gate_dict[gate].remove(self.ship)
                return "S21"
            else:
                return

        elif state == "S21":
            if input == "\n":
                return "S8"
            else:
                return

        elif state == "S22":
            if input == "\n":
                return "S8"
            else:
                return

        elif state == "S23":
            if input == "\n":
                return "S1"
            else:
                return "S23"

        elif state == "S24":
            if input =="\n":
                return "S8"
            else:
                return "S24"
        else:
            return None


    def entry(self, state, input):
        pass


if __name__ == "__main__":
    file_list = ["output_trace.txt"]
    for i in range(1,7):
        file_list.append(f"trace{i}.txt")
    for file_name in file_list:
        print(f"{file_name}" )
        file = open(file_name, mode='r')
        stream_string = file.read()
        file.close()
        stream = CharacterStream(stream_string)
        scanner = Req4Scanner(stream)
        success = scanner.scan()
        if success:
            print("Stream has been accepted.")
        else:
            print(f"Stream not accepted: A ship is crushed at gate: G{str(scanner.gate)}.\n"
                  f"The following ships are crushed {str(scanner.gate_dict[scanner.gate])}.")
        # if success:
        #     print("Stream has been accepted.")
        # else:
        #     print(f"Stream not accepted: Problem with gate: G{str(scanner.number)}.\n"
        #           f"Gates {str(scanner.gate_list)} are open.")
        print("")