# togirBotRelease
 My own bot for telegram

<h1>Commands</h1>
🐷 <b>Возможности админов группы:</b><br>
/kick <i>(ответ на сообщение пользователя или айди)</i> - удалить пользователя из группы<br>
/del <i>(ответ на сообщение)</i> - удалить сообщение анонимно<br>

😍 <b>Возможности админов бота:</b><br>
/type - получить готовый шаблон сообщения для /replyTo<br>
/replyTo <i>(chat_id) (message_id) (text)</i> - отвечает на опредленное сообщение в определенном чате<br>
/send <i>(chat_id) (text)</i> - отправить сообщщение в определенный чат<br>
/stop <i>(время в минутах) (текст)</i> - останавливает бота на определенное количество минут<br>
/getUsers - получить количество юзеров в базе данных<br>
/getChats - получить количество груп в базе данных<br>
/sendAllChats (text) - сделать рассылку всем группам<br>
/sendAllUsers (text) - сделать рассылку всем пользователям<br>

🐵 <b>Возможности для разработчиков:</b> <i>(эти команды доступны для всех)</i><br>
/len - узнать длину сообщения<br>
/get - получить айди чата<br>
/getId - получить айди пользователя на которого вы ответили<br>
/getMessageId - получить айди сообщения на которого вы ответили<br>
