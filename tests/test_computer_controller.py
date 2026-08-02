from aura.computer.controller import ComputerController


def test_computer_controller_rejects_unknown_action():

    controller = ComputerController()

    result = controller.execute_action(
        "unknown",
    )

    assert "Unsupported" in result
