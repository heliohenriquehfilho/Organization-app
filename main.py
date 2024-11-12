from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.storage.jsonstore import JsonStore
from kivy.uix.scrollview import ScrollView
from datetime import datetime


"""
Feito -> 01 - Adicionar Aulas
Feito -> 02 - Remover Aulas
Feito -> 03 - Adicionar Tarefas
Feito -> 04 - Concluir Tarefas
Feito -> 05 - Remover Tarefas
Feito -> 06 - Salvar Progresso
07 - Gráfico Progresso
08 - Adicionar Peso
09 - Adicionar água
10 - Adicionar Datas Importantes
11 - Calendário
12 - Login
"""


class MainMenu(Widget):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.Aulas = {}

        self.store = JsonStore("user_data.json")

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.width = 400
        self.layout.height = 500
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Botão inicial para adicionar aula
        self.add_aula = Button(text="Adicionar Aula", size_hint=(1, None), height=50)
        self.add_aula.bind(on_press=self.add_aulas_estrutura)

        self.remover_aula_butao = Button(text='Remover Aula', size_hint=(1, None), height=50)
        self.remover_aula_butao.bind(on_press=self.remover_aulas)

        self.tarefas_button = Button(text="Tarefas", size_hint =(1, None),height=50)
        self.tarefas_button.bind(on_press=self.tarefas_pagina)
        self.layout.add_widget(self.tarefas_button)

        self.layout.add_widget(self.add_aula)
        self.layout.add_widget(self.remover_aula_butao)
        self.add_widget(self.layout)


    def tarefas_pagina(self, instance):
        self.clear_widgets()
        self.add_widget(TarefasWindow())


    def add_aulas_estrutura(self, instance):
        # Layout vertical para organizar o input, os checkboxes e o botão de salvar
        self.aula_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Campo de entrada para o nome da aula
        self.nome_input = TextInput(hint_text="Qual o nome da aula?", size_hint=(1, None), height=50)
        self.aula_layout.add_widget(self.nome_input)
        
        # Layout para os dias da semana
        dias_layout = BoxLayout(orientation='horizontal', spacing=10)
        dias_label = Label(text="Dias:", size_hint=(None, None), width=50, height=50)
        dias_layout.add_widget(dias_label)
        
        # Dicionário para armazenar os checkboxes dos dias
        self.dias_checkboxes = {}
        dias_semana = {2: "Seg", 3: "Ter", 4: "Qua", 5: "Qui", 6: "Sex"}
        
        # Cria um checkbox para cada dia da semana
        for dia_num, dia_nome in dias_semana.items():
            dia_checkbox = CheckBox(size_hint=(None, None), width=30, height=30)
            self.dias_checkboxes[dia_num] = dia_checkbox
            dia_layout = BoxLayout(orientation='vertical', size_hint=(None, None), width=50, height=50)
            dia_layout.add_widget(Label(text=dia_nome, size_hint=(None, None), height=20))
            dia_layout.add_widget(dia_checkbox)
            dias_layout.add_widget(dia_layout)

        self.aula_layout.add_widget(dias_layout)

        # Layout para os horários
        horarios_layout = BoxLayout(orientation='horizontal', spacing=10)
        horarios_label = Label(text="Horários:", size_hint=(None, None), width=80, height=50)
        horarios_layout.add_widget(horarios_label)
        
        # Dicionário para armazenar os checkboxes dos horários
        self.horarios_checkboxes = {}
        horarios = ["M12", "M34", "T12", "T34", "N12", "N34"]
        
        # Cria um checkbox para cada horário
        for horario in horarios:
            horario_checkbox = CheckBox(size_hint=(None, None), width=30, height=30)
            self.horarios_checkboxes[horario] = horario_checkbox
            horario_layout = BoxLayout(orientation='vertical', size_hint=(None, None), width=50, height=50)
            horario_layout.add_widget(Label(text=horario, size_hint=(None, None), height=20))
            horario_layout.add_widget(horario_checkbox)
            horarios_layout.add_widget(horario_layout)

        self.aula_layout.add_widget(horarios_layout)

        # Botão para salvar a aula
        self.save_button = Button(text="Adicionar a agenda", size_hint=(1, None), height=50)
        self.save_button.bind(on_press=self.add_aulas_back)
        self.aula_layout.add_widget(self.save_button)

        # Adiciona o layout de aula ao layout principal
        self.layout.add_widget(self.aula_layout)

        # Remove o botão inicial para evitar duplicação
        self.layout.remove_widget(self.add_aula)


    def add_aulas_back(self, instance):
        # Coleta o nome da aula
        nome_aula = self.nome_input.text

        # Coleta os dias selecionados
        dias_selecionados = [dia for dia, checkbox in self.dias_checkboxes.items() if checkbox.active]

        # Coleta os horários selecionados
        horarios_selecionados = [horario for horario, checkbox in self.horarios_checkboxes.items() if checkbox.active]

        # Salva a aula no dicionário
        self.Aulas[nome_aula] = {
            "dias": dias_selecionados,
            "horarios": horarios_selecionados
        }

        # Recupera as aulas existentes (se houver) e adiciona a nova aula
        if self.store.exists("user1"):
            existing_data = self.store.get("user1")
            existing_data["aulas"].update(self.Aulas)
            self.store.put("user1", aulas=existing_data["aulas"])
        else:
            self.store.put("user1", aulas=self.Aulas)

        # Remove os widgets de entrada e o botão de salvar
        self.layout.remove_widget(self.aula_layout)

        # Adiciona o botão inicial novamente
        self.layout.add_widget(self.add_aula)
        
        # Debug print para verificar o que foi salvo
        print(self.Aulas)
        
        return self.Aulas
    

    def remover_aulas(self, instance):

        aulas_escolha = DropDown()

        self.mainbutton = Button(text='Escolha a Aula', size_hint=(None, None))

        # Adiciona um botão para cada aula existente no dicionário Aulas
        for nome_aula in self.Aulas.keys():
            # Cria um botão para cada aula
            bttn = Button(text=nome_aula, size_hint_y=None, height=44)
            
            # Define a ação ao selecionar uma aula
            bttn.bind(on_release=lambda btn: self.remover_aula(btn.text))
            
            # Adiciona o botão ao DropDown
            aulas_escolha.add_widget(bttn)

        # Vincula o DropDown ao botão principal
        self.mainbutton.bind(on_release=aulas_escolha.open)

        # Adiciona o DropDown à interface
        self.layout.add_widget(self.mainbutton)


    def remover_aula(self, nome_aula):
        # Remove a aula do dicionário
        if nome_aula in self.Aulas:
            del self.Aulas[nome_aula]
            print(f"Aula '{nome_aula}' removida. Aulas restantes: {self.Aulas}")

            self.layout.remove_widget(self.mainbutton)
        else:
            print(f"Aula '{nome_aula}' não encontrada.")


class TarefasWindow(Widget):
    def __init__(self, **kwargs):
        super(TarefasWindow, self).__init__(**kwargs)

        self.store = JsonStore("user_data.json")

        # Carregar tarefas do usuário se existirem
        self.tasks = self.store.get("user1").get("tasks", {}) if self.store.exists("user1") else {}

        # Layout principal
        self.tarefas_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.tarefas_layout.width = 300
        self.tarefas_layout.height = 400
        self.tarefas_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Título
        self.titulo = Label(text="Tarefas", size_hint=(1, None), height=40)
        self.tarefas_layout.add_widget(self.titulo)

        # Botão para adicionar tarefa
        self.add_task_button = Button(text="Adicionar Tarefa", size_hint=(1, None), height=50)
        self.add_task_button.bind(on_press=self.add_task)
        self.tarefas_layout.add_widget(self.add_task_button)

        # Botão para remover tarefas concluídas
        self.remove_task_button = Button(text="Remover Tarefas Concluídas", size_hint=(1, None), height=50)
        self.remove_task_button.bind(on_press=self.remove_completed_tasks)
        self.tarefas_layout.add_widget(self.remove_task_button)

        self.return_home_button = Button(text="Retornar a Página Principal")
        self.return_home_button.bind(on_press=self.return_home)
        self.tarefas_layout.add_widget(self.return_home_button)

        # Campo de entrada de nova tarefa
        self.task_input = TextInput(hint_text="Digite a tarefa", size_hint=(1, None), height=40)
        self.tarefas_layout.add_widget(self.task_input)

        # Lista de tarefas (ScrollView)
        self.task_list_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.task_list_layout.bind(minimum_height=self.task_list_layout.setter('height'))
        
        self.task_list_scroll = ScrollView(size_hint=(1, 1))
        self.task_list_scroll.add_widget(self.task_list_layout)
        
        self.tarefas_layout.add_widget(self.task_list_scroll)

        # Dicionário para armazenar tarefas e seus checkboxes
        self.tasks = {}

        # Adiciona o layout de tarefas ao widget
        self.add_widget(self.tarefas_layout)

    def return_home(self, instance):
        self.clear_widgets()
        self.add_widget(MainMenu())

    def add_task(self, instance):
        """Adiciona uma nova tarefa à lista e salva no arquivo JSON do usuário."""
        task_text = self.task_input.text.strip()
        
        if task_text:
            # Layout horizontal para cada tarefa
            task_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

            # Checkbox para marcar a tarefa como concluída
            checkbox = CheckBox(size_hint=(None, None), width=30, height=30)
            task_layout.add_widget(checkbox)

            # Label com o nome da tarefa
            task_label = Label(text=task_text, size_hint=(1, None), height=40)
            task_layout.add_widget(task_label)

            # Adiciona o layout da tarefa à lista de tarefas visíveis
            self.task_list_layout.add_widget(task_layout)

            # Adiciona a nova tarefa ao dicionário de tarefas do usuário
            self.tasks[task_text] = False  # Inicia como não concluída

            # Atualiza o arquivo JSON com as tarefas do usuário "user1"
            if self.store.exists("user1"):
                existing_data = self.store.get("user1")
                # Atualiza o dicionário de tarefas com a nova tarefa
                existing_data["tasks"].update(self.tasks)
                self.store.put("user1", **existing_data)
            else:
                self.store.put("user1", tasks=self.tasks)

            # Limpa o campo de entrada
            self.task_input.text = ""

    def remove_completed_tasks(self, instance):
        """Remove tarefas que estão marcadas como concluídas e atualiza o JSON com a data de conclusão."""
        completed_tasks = [task for task, is_active in self.tasks.items() if not is_active]  # Tarefas concluídas

        for task in completed_tasks:
            # Encontre e remova o layout correspondente na interface
            for task_layout in self.task_list_layout.children[:]:  # Iterando pela lista de layouts
                # Encontre o Label dentro do layout da tarefa
                task_label = next((widget for widget in task_layout.children if isinstance(widget, Label)), None)
                
                if task_label and task_label.text == task:
                    self.task_list_layout.remove_widget(task_layout)  # Remove o layout da interface
                    break  # Tarefa encontrada, interrompe o loop

            # Registra a data e a hora de conclusão no JSON
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Atualiza a tarefa no JSON com o status de concluída e a data e hora
            if self.store.exists("user1"):
                existing_data = self.store.get("user1")
                if "tasks" in existing_data and task in existing_data["tasks"]:
                    existing_data["tasks"][task] = {
                        "completed": True,
                        "completion_time": completion_time
                    }
                self.store.put("user1", **existing_data)

            # Remove a tarefa do dicionário local de tarefas
            del self.tasks[task]
            
class MainWindow(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    MainWindow().run()
