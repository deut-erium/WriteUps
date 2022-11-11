import base64

tokens = {
    'a':"eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJhIn0.wN0kGlDUj5n8x6GGptROB2PskEeOHe-ONvXE6VDWevt6G3cq4fkWogQrMAp6mBgX0nkiB6lbAasqVmzaFs3Xfg",
    "b":"eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJiIn0.wN0kGlDUj5n8x6GGptROB2PskEeOHe-ONvXE6VDWevsj43wUm4vcSSFPx8SEXdQBlZGbQKQ2UUKpZ6wMUBryLg",
    "c":"eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJjIn0.wN0kGlDUj5n8x6GGptROB2PskEeOHe-ONvXE6VDWevuyaFH4dSoTBoDdAcbWo4LC8FPWlsBPufLxd4R1_P3W_w",
    "d":"eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJkIn0.wN0kGlDUj5n8x6GGptROB2PskEeOHe-ONvXE6VDWevv7vRjRoXe0HkqQC90YEGLZ0QgMN5ffA05UbQSGPODBwg",
    "e":"eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJlIn0.wN0kGlDUj5n8x6GGptROB2PskEeOHe-ONvXE6VDWevvA6DCUMupO0eDFaR75o3pRA6aDFvAmlCgcM1trjPcMkw",
    "f":"eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJmIn0.wN0kGlDUj5n8x6GGptROB2PskEeOHe-ONvXE6VDWevuk05uGQhklCAz-yY-HgJzygrWrNIhm1KP9RHjXyYKpwg",
    "admin{":"eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJhZG1pbnsifQ.wN0kGlDUj5n8x6GGptROB2PskEeOHe-ONvXE6VDWevv-fO_nrLjxGa8c0f-6H6nCvDi4WtS1PZBPq_Pi_r3axw",
    "ADMIN":"eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJBRE1JTiJ9.wN0kGlDUj5n8x6GGptROB2PskEeOHe-ONvXE6VDWevvxvRZHKuUcMBh93GZVN2y6reGwolyDFS97Fu8CcdHIJw"
}
def s(username):
	body = '{' \
              + '"admin": "' + "False" \
              + '", "username": "' + str(username) \
              + '"}'
	return body
