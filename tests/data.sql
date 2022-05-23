INSERT INTO user (email, username, password)
VALUES ('test.user@gmail.com', 'test_user',
        'pbkdf2:sha256:260000$4lFvMN0bfpkhHE1f$3856dec3982be3e9246e1171c88d6591ca68959eb3452c1c4807976392feaa0a'),
       ('other.user@gmail.com', 'other_user',
        'pbkdf2:sha256:260000$cuxhTLsUONw6HIij$2e14fe5f6a9a28f0e608173e2ea4eb9975483a5f8ec628c2194ea15bde4b0fba');


INSERT INTO comments (content, parent, username, created_time)
VALUES ('test_content', 0, 'test_user', '2022-05-21 00:00:00');