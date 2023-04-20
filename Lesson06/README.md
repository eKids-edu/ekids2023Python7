# Заняття №6

## План практичного заняття

* Створити секцію `__main__`
* Створити функцію для завантаження списку товарів `load()` та використати її
* Створити функцію для збереження списку товарів `save()`
  та використати її у `add_goods()` та `delete_goods()`
* Додати до властивостей товару "Кількість", та змінну `PRIMARY_KEY`
* Розповісти філософію застосування функцій:
  * DRY
  * легке читання коду та простіше працювати з ним
* Оновити функцію додавання товару `add_goods()`:
  * Зробити функцію парсингу команди `parse_command_args()` із допоміжними
    функціями `skip_command_and_split()` та `delete_spaces()`
  * Зробити функцію перевірки наявності товару `find_goods()`
  * Зробити функції встановлення/перевірки ціни та кількості
    товару `set_price()` та `set_stock()`
* Оновити функцію видалення товару `delete_goods()`:
  * Використати функції `parse_command_args()` та `find_goods()` з
    їх допомогою зробити можливість видаляти одразу декілька товарів
* Розповісти що `message.chat.id` дозволяє використовувати бота в групах
* Оновити функції `send_help()` та `send_welcome()`

## Результат заняття

Ми навчилися писати функції та використовувати їх у нашому коді для
запобігання повторів а також для того, щоб код був більш простим
для читання та подальшої роботи з ним.

Пристосували бот для роботи в групах.