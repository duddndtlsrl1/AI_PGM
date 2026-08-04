#include <functional>
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include <GLFW/glfw3.h>
#include <string>
#include <cmath>

// 계산기 상태 변수
std::string g_current = "0";
double g_operand = 0.0;
std::string g_operator = "";
bool g_newNumber = true;

// 숫자 정규화 (.0 제거)
std::string NormalizeNumber(double value) {
    if (value == (int)value) {
        return std::to_string((int)value);
    }
    return std::to_string(value);
}

// 순수 계산 함수
double PerformOperation(double a, double b, const std::string& op) {
    if (op == "+") return a + b;
    if (op == "-") return a - b;
    if (op == "×") return a * b;
    if (op == "÷") {
        if (b == 0) throw std::string("ZeroDivisionError");
        return a / b;
    }
    return b;
}

// 숫자 입력
void InputNumber(int n) {
    std::string nStr = std::to_string(n);
    if (g_newNumber) {
        g_current = nStr;
        g_newNumber = false;
    }
    else {
        if (g_current == "0") g_current = nStr;
        else g_current += nStr;
    }
}

// 소수점 입력
void InputDot() {
    if (g_newNumber) {
        g_current = "0.";
        g_newNumber = false;
    }
    else if (g_current.find('.') == std::string::npos) {
        g_current += ".";
    }
}

// 연산자 입력
void InputOperation(const std::string& op) {
    double currentVal = std::stod(g_current);
    if (g_operator.empty()) {
        g_operand = currentVal;
    }
    else if (!g_newNumber) {
        try {
            g_operand = PerformOperation(g_operand, currentVal, g_operator);
            g_current = NormalizeNumber(g_operand);
        }
        catch (...) {
            g_current = "Error";
        }
    }
    g_operator = op;
    g_newNumber = true;
}

// 계산 실행 (=)
void Calculate() {
    if (g_operator.empty()) return;
    double currentVal = std::stod(g_current);
    try {
        double result = PerformOperation(g_operand, currentVal, g_operator);
        g_current = NormalizeNumber(result);
        g_operand = 0;
        g_operator = "";
        g_newNumber = true;
    }
    catch (...) {
        g_current = "Error";
        g_operand = 0;
        g_operator = "";
        g_newNumber = true;
    }
}

// Clear
void ClearAll() {
    g_current = "0";
    g_operand = 0.0;
    g_operator = "";
    g_newNumber = true;
}

// Backspace
void Backspace() {
    if (g_current.length() > 1) {
        g_current.pop_back();
    }
    else {
        g_current = "0";
    }
}

// 부호 변환 (±)
void ToggleSign() {
    if (g_current != "0") {
        if (g_current[0] == '-') g_current = g_current.substr(1);
        else g_current = "-" + g_current;
    }
}

int main() {
    // 1. GLFW 초기화
    if (!glfwInit()) return 1;

    GLFWwindow* window = glfwCreateWindow(380, 600, "Calculator (ImGui)", NULL, NULL);
    if (!window) { glfwTerminate(); return 1; }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    // 2. Dear ImGui 초기화
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO(); (void)io;
    ImGui::StyleColorsDark();

    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init("#version 130");

    // 3. 메인 루프
    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        // 창 크기를 고정하거나 전체를 채우는 윈도우 생성
        ImGui::SetNextWindowPos(ImVec2(0, 0));
        ImGui::SetNextWindowSize(ImGui::GetIO().DisplaySize);
        ImGuiWindowFlags flags = ImGuiWindowFlags_NoTitleBar | ImGuiWindowFlags_NoResize |
            ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoScrollbar;

        ImGui::Begin("Calculator", NULL, flags);

        // 스타일 설정 (다크모드 맞춤)
        ImGui::PushStyleColor(ImGuiCol_Button, ImVec4(0.18f, 0.18f, 0.18f, 1.0f));
        ImGui::PushStyleColor(ImGuiCol_ButtonHovered, ImVec4(0.3f, 0.3f, 0.3f, 1.0f));
        ImGui::PushStyleColor(ImGuiCol_ButtonActive, ImVec4(0.4f, 0.4f, 0.4f, 1.0f));

        // 히스토리 영역
        std::string historyStr = "";
        if (!g_operator.empty()) {
            historyStr = NormalizeNumber(g_operand) + " " + g_operator;
        }
        ImGui::PushStyleColor(ImGuiCol_Text, ImVec4(0.66f, 0.66f, 0.66f, 1.0f));
        ImGui::Text("%s", historyStr.c_str());
        ImGui::PopStyleColor();

        // 결과 디스플레이 영역
        ImGui::PushStyleColor(ImGuiCol_Text, ImVec4(1.0f, 1.0f, 1.0f, 1.0f));
        // 우측 정렬 느낌을 주기 위한 빈 공간 배치 혹은 폰트 크기 조절 가능
        ImGui::SetCursorPosX(ImGui::GetWindowWidth() - ImGui::CalcTextSize(g_current.c_str()).x - 20);
        ImGui::Text("%s", g_current.c_str());
        ImGui::PopStyleColor();

        ImGui::Spacing();
        ImGui::Separator();
        ImGui::Spacing();

        // 버튼 그리드 배치 (4열)
        float btnWidth = 80.0f;
        float btnHeight = 55.0f;

        auto ButtonGrid = [&](const char* label, std::function<void()> func) {
            if (ImGui::Button(label, ImVec2(btnWidth, btnHeight))) {
                func();
            }
            ImGui::SameLine();
            };

        ButtonGrid("%", [] { g_current = NormalizeNumber(std::stod(g_current) / 100.0); });
        ButtonGrid("CE", ClearAll);
        ButtonGrid("C", ClearAll);
        ButtonGrid("⌫", Backspace);
        ImGui::NewLine();

        ButtonGrid("1/x", [] { double v = std::stod(g_current); g_current = (v == 0) ? "Error" : NormalizeNumber(1 / v); });
        ButtonGrid("x²", [] { double v = std::stod(g_current); g_current = NormalizeNumber(v * v); });
        ButtonGrid("√x", [] { double v = std::stod(g_current); g_current = (v < 0) ? "Error" : NormalizeNumber(sqrt(v)); });
        ButtonGrid("÷", [] { InputOperation("÷"); });
        ImGui::NewLine();

        ButtonGrid("7", [] { InputNumber(7); });
        ButtonGrid("8", [] { InputNumber(8); });
        ButtonGrid("9", [] { InputNumber(9); });
        ButtonGrid("×", [] { InputOperation("×"); });
        ImGui::NewLine();

        ButtonGrid("4", [] { InputNumber(4); });
        ButtonGrid("5", [] { InputNumber(5); });
        ButtonGrid("6", [] { InputNumber(6); });
        ButtonGrid("-", [] { InputOperation("-"); });
        ImGui::NewLine();

        ButtonGrid("1", [] { InputNumber(1); });
        ButtonGrid("2", [] { InputNumber(2); });
        ButtonGrid("3", [] { InputNumber(3); });
        ButtonGrid("+", [] { InputOperation("+"); });
        ImGui::NewLine();

        ButtonGrid("±", ToggleSign);
        ButtonGrid("0", [] { InputNumber(0); });
        ButtonGrid(".", InputDot);
        ButtonGrid("=", Calculate);

        ImGui::PopStyleColor(3);
        ImGui::End();

        // 렌더링
        ImGui::Render();
        int display_w, display_h;
        glfwGetFramebufferSize(window, &display_w, &display_h);
        glViewport(0, 0, display_w, display_h);
        glClearColor(0.12f, 0.12f, 0.12f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        glfwSwapBuffers(window);
    }

    // 정리
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();

    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}