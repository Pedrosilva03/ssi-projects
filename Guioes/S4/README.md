# Respostas das Questões

## Q2
Um NONCE fixo é muito mais fácil de decifrar pois ao decifrar diferentes mensagens com o mesmo NONCE, são criados padrões nas mensagens cripografadas que podem ser detetados e decifrados por possíveis atacantes.

## Q3
O modo CBC é mais vulnerável ao ```chacha20_int_attck.py``` pois este pode ser usado para manipular partes do texto criptografado ou seja se um atacante souber partes do texto e a posição, pode alterar conteúdo da mensagem original

O modo CTR é menos vulnerável pois a cifra e aleatória então torna as manipulações muito mais difíceis de serem feitas.