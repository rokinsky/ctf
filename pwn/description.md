Zawartość pliku `flag.txt` w katalogu bieżącym serwera: `BSK{s1mpl3-r0p-1s-5imp1e}`

Zacząłem od sprawdzenia włączanych zabezpieczeń pliku binarnego programu za pomocą polecenia `checksec` w `pwndbg`: 

    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled

z czego wywnioskowałem, że sensownym pomysłem jest skorzystanie z ROPGadgetoów.

Widać, że operacja `APPEND_T` jest wadliwym miejscem programu i można to wykorzystać do przepełnienia bufora robiąc pełny `READ_T` i po nim `APPEND_T`.

Zauważyłem, że w programie po odczycie danych jest wykonywana funkcja `memfrob` na otrzymanym obiekcie, więc przed wysyłaniem danych do programu wykonuje analogiczną funkcję, ponieważ xor jest grupą 2-elementową. 

Wyłapywanie kanarka wygląda standardowo - jak na zajęciach. Z wyłączonym ASLRem i swoim libcem napisałem wywołanie shella ze stałym adresem. Po znalezieniu odpowiedniego offseta pomiędzy kanarkiem a ROPgadgetami udało się uruchomić shella lokalnie.

Za pomocą adresu `__libc_start_main + offset` na stosie udało się wyciągnąć adres libca i zatem obejść ASLR. Została tylko zamiana offsetów libca, które dostałem wykonująć poniższe komendy:

```
readelf -Ws libc.so.6 | grep "system@@" && \
readelf -Ws libc.so.6 | grep "__libc_start_main@@" && \
strings -tx libc.so.6 | grep "bin/sh" && \
ROPgadget --binary libc.so.6 | grep "pop rdi ; ret"
```

Powstały po drodze skrypt jest w pliku `exploit.py`
