
CREATE TABLE notification_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email          VARCHAR(255)      NOT NULL,
    company_symbol      VARCHAR(50)       NOT NULL,
    threshold           DECIMAL(10,2)     NOT NULL,
    comparison_operator ENUM('>=', '<')    NOT NULL,
    event_active        BOOLEAN           NOT NULL DEFAULT FALSE,
    enabled             BOOLEAN           NOT NULL DEFAULT TRUE
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_id  INT          NOT NULL,
    sent_at  DATETIME     NOT NULL,
    FOREIGN KEY (rule_id) REFERENCES notification_rules(id)
);
