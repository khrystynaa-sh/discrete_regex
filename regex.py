from __future__ import annotations
from abc import ABC, abstractmethod
import argparse




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
    def __init__(self, symbol: str):
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
    def __init__(self, pattern: str):
        self.start_state = StartState()
        prev = self.start_state

        i = 0
        while i < len(pattern):
            char = pattern[i]

            if i + 1 < len(pattern) and pattern[i + 1] in "*+":
                op = pattern[i + 1]
                base = self._make_state(char)
                if op == "*":
                    star = StarState(base)
                    prev.next_states.append(star)
                    prev.next_states.append(base)
                    base.next_states.append(star)
                    prev = star
                elif op == "+":
                    plus = PlusState(base)
                    prev.next_states.append(base)
                    base.next_states.append(plus)
                    plus.next_states.append(base)
                    prev = plus
                i += 2
                continue
            state = self._make_state(char)
            prev.next_states.append(state)
            prev = state
            i += 1

        prev.next_states.append(TerminationState())

    def _make_state(self, token: str) -> State:
        if token == ".":
            return DotState()
        return AsciiState(token)


    def check_string(self, s: str) -> bool:
        visited = set()

        def dfs(state: State, idx: int) -> bool:
            if (id(state), idx) in visited:
                return False
            visited.add((id(state), idx))

            if isinstance(state, TerminationState):
                return idx == len(s)
            if idx < len(s):
                for nxt in state.next_states:
                    if nxt.check_self(s[idx]):
                        if dfs(nxt, idx + 1):
                            return True
            for nxt in state.next_states:
                if isinstance(nxt, (StarState, PlusState)):
                    if dfs(nxt, idx):
                        return True

            return False

        return dfs(self.start_state, 0)



def main():
    parser = argparse.ArgumentParser(description="Simple FSM Regex Engine")
    parser.add_argument("regex", help="Pattern (supports ., * and +)")
    parser.add_argument("string", help="Input string")

    args = parser.parse_args()

    fsm = RegexFSM(args.regex)
    print(fsm.check_string(args.string))


if __name__ == "__main__":
    main()
