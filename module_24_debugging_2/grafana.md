## Подключение Grafana

### Пример по настройке [dashboard](https://github.com/rycus86/prometheus_flask_exporter/tree/master/examples/sample-signals) в grafana

* СОДЕРЖАНИЕ
  * Создать [Data Source](#создаем-источник-данных)
  * Добавить [Panel](#здесь-будем-фильтровать-по-status_code-200)
  * Работаем с [JSON](#сохраняем-json)

<hr>

* В файле *docker-compose* мы создали контейнер с подключением **grafana**
```html
    # Подключение визуализации мониторинга "Grafana"
  grafana:
    image: grafana/grafana:5.1.0
    ports:
      - "3000:3000"
```

* После запуска сервера, к **Grafana** будет доступ по пути
```html
http://localhost:3000
```
* Появится окно с вводом логина и пароля (по умолчанию **admin** / **admin**)

<img src="img_docs/login.png" width="600px">

### Создаем источник данных

<img src="img_docs/create_date_source.png" width="600px">

* Настраиваем источник данных (выбираем **Prometheus**, задаем имя, определяем адрес и порт источника)

<img src="img_docs/setting_data_source.png" width="600px">

* Нажимаем **Save and test**, если все верно появиться надпись **Data source is working**. Далее нажимаем **Back** 

### Настраиваем Dashboard

<img src="img_docs/new_dashboard.png" width="600px">

* Создаем панель **Graph**

<img src="img_docs/add_graph.png" width="600px">

* В следующем окне выбираем **Edit**

<img src="img_docs/edit_panel.png" width="600px">

### Здесь будем фильтровать по status_code 200

* В поле **Data Source** выбираем наш источник данных

<img src="img_docs/select_data_source.png" width="600px">

* Переходим по адресу **http://localhost:5000/metrics** прежде посетив наши *endpoints*
Перед нами появится страница с метриками, Вот часть из всей информации

<img src="img_docs/metrics.png" width="600px">

* Для нашей задачи интересуют переменные которые мы определили для наших **endpoints**
с суффиксом `**_total**`
```html
# т.е. для endpoint `index`
doors_app_counter_index_total{status="200"} 5.0

# где 5.0 - это наш счетчик посещений страницы
```

<img src="img_docs/variable_for_endpoint.png" width="800px">

* Вводим эту переменную, задаем ей имя для отображения на панели
* Если требуется добавить еще точек нажмите кнопку **Add Query** 

<img src="img_docs/add_variable.png" width="600px">

* Для более хорошей визуализации можно настроить поле **Legend**

<img src="img_docs/setting_legend.png" width="600px">

* И в правом верхнем углу отобразятся наши точки

<img src="img_docs/select_legend_2.png" width="600px">

* Сохраняем наши настройки

<img src="img_docs/save_panel.png" width="600px">

* Задаем имя нашей сборки

<img src="img_docs/save_panel_name.png" width="600px">

### Добавить график и отфильтровать по status_code 500 - аналогично предыдущему фильтру

## Итого

<img src="img_docs/visualize.png" width="700px">

<hr>

### Сохраняем json

* После сохранения настроек **Dashboard** можем сохранить все данные в файл **json**
* Для этого зайдем в настройки

<img src="img_docs/settings_btn.png" width="600px">

* И выбираем меню **View JSON**

<img src="img_docs/view_json.png" width="700px">

* Копируете все содержимое файла и сохраняете у себя (можно в проекте)
* Например:

<img src="img_docs/save_json.png">

<hr>

### Итого

* При последующем подключении: 
* Вам потребуется снова создать источник данных;
* И импортировать **json** с настройками

<img src="img_docs/1.png" width="700px">
<img src="img_docs/2.png" width="700px">
<img src="img_docs/3.png" width="700px">
<img src="img_docs/4.png" width="700px">
