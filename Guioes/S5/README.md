# Respostas das Questões
## Q1
O impacto de executar o programa chacha20_int_attck.py sobre um criptograma produzido por pbenc_chacha20_poly1305.py seria mínimo ou inexistente. Isso ocorre porque a cifra ChaCha20-Poly1305 é uma construção de criptografia autenticada, que inclui um código de autenticação de mensagem (MAC) para garantir a autenticidade e integridade dos dados.
O ataque implementado pelo script chacha20_int_attck.py envolve a modificação do texto-limpo em uma posição específica e, em seguida, a recalculação do keystream e a modificação do criptograma correspondente. No entanto, o Poly1305, que é usado para autenticação na cifra ChaCha20-Poly1305, é uma função de hash de mensagem autenticada (HMAC) que garante a integridade do texto-limpo.
Se o ataque modificar o texto-limpo em uma posição específica, a função Poly1305 calculará um MAC diferente durante a verificação da autenticidade, indicando que a mensagem foi alterada. Portanto, a autenticação proporcionada pelo Poly1305 impediria a aceitação de um criptograma modificado sem a chave correta.

## Q2
Usa-se uma mensagem de mais de 16 bytes para que o último bloco permaneça o mesmo ao manipular a tag pelo facto de que o AES tem um tamanho de bloco limitado a 16 bytes.