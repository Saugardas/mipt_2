CREATE TYPE action_type AS ENUM ('start', 'help', 'request', 'answer', 'error');

CREATE TABLE bot_logs (
	id serial primary key,
	user_id bigint, -- может быть пустым, если сохраняем внутренние ошибки
	action action_type NOT NULL,
	additional_info varchar(50), -- сообщение об ошибке или запрос пользователя
	created_at TIMESTAMP DEFAULT NOW()
);