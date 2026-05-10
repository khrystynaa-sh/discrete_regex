from __future__ import annotations
from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self):
        self.next_states: list[State] = []

    @abstractmethod
    def check_self(self, char: str) -> bool:
        pass


class StartState(State):
    def check_self(self, char: str) -> bool:
        return False


class TerminationState(State):
    def check_self(self, char: str) -> bool:
        return False


class DotState(State):
    def check_self(self, char: str) -> bool:
        return True


class AsciiState(State):
    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol

    def check_self(self, char: str) -> bool:
        return char == self.symbol


class StarState(State):
    def __init__(self, inner: State):
        super().__init__()
        self.inner = inner
        self.next_states.append(self)

    def check_self(self, char: str) -> bool:
        return self.inner.check_self(char)


class PlusState(State):
    def __init__(self, inner: State):
        super().__init__()
        self.inner = inner

    def check_self(self, char: str) -> bool:
        return self.inner.check_self(char)


class RegexFSM:
    def __init__(self, regex_expr: str) -> None:
        self.start_state = StartState()
        prev_state = self.start_state

        i = 0
        while i < len(regex_expr):
            char = regex_expr[i]

            if i + 1 < len(regex_expr) and regex_expr[i + 1] in "*+":
                op = regex_expr[i + 1]
                base = self.__make_state(char)
                if op == "*":
                    star = StarState(base)
                    prev_state.next_states.append(star)
                    prev_state.next_states.append(base)
                    base.next_states.append(star)
                    prev_state = star
                elif op == "+":
                    plus = PlusState(base)
                    prev_state.next_states.append(base)
                    base.next_states.append(plus)
                    plus.next_states.append(base)
                    prev_state = plus
                i += 2
                continue

            state = self.__make_state(char)
            prev_state.next_states.append(state)
            prev_state = state
            i += 1

        prev_state.next_states.append(TerminationState())

    def __make_state(self, token: str) -> State:
        if token == ".":
            return DotState()
        elif token.isascii():
            return AsciiState(token)
        else:
            raise ValueError("Unsupported character")

    def check_string(self, input_str: str) -> bool:
        visited = set()

        def dfs(state: State, idx: int) -> bool:
            if (id(state), idx) in visited:
                return False
            visited.add((id(state), idx))

            if isinstance(state, TerminationState) and idx == len(input_str):
                return True
            if idx < len(input_str):
                for nxt in state.next_states:
                    if nxt.check_self(input_str[idx]):
                        if dfs(nxt, idx + 1):
                            return True
            for nxt in state.next_states:
                if dfs(nxt, idx):
                    return True

            return False

        return dfs(self.start_state, 0)


if __name__ == "__main__":
    regex_pattern = "a*4.+hi"
    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))        # True
    print(regex_compiled.check_string("meow"))        # False
