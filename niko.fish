# >>> Niko Terminal >>>
# Fish gère le dessin comme une invite multiligne et le redessine au resize.
function fish_greeting
end

if status is-interactive; and test "$TERM" != dumb
    if not functions -q __niko_original_prompt
        functions --copy fish_prompt __niko_original_prompt
    end

    function fish_prompt
        # Calculer d'abord l'invite habituelle pour conserver le statut précédent.
        set --local original_prompt (__niko_original_prompt $argv | string collect)
        if not contains -- --final-rendering $argv
            if test -x "$HOME/.local/bin/niko-banner"
                command env COLUMNS=$COLUMNS LINES=$LINES "$HOME/.local/bin/niko-banner"
            end
        end
        printf '%s' "$original_prompt"
    end

    # Retirer le dessin de l'ancienne invite quand une commande est exécutée.
    set --global fish_transient_prompt 1

    function __niko_resize --on-signal WINCH
        commandline --function repaint 2>/dev/null
    end
end
# <<< Niko Terminal <<<
