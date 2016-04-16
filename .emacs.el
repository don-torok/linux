
;; Hide password
(add-hook 'comint-output-filter-functions
'comint-watch-for-password-prompt)


;; Dont echo the password when logging in form the emacs shell
(add-hook 'comint-output-filter-functions
      'comint-watch-for-password-prompt)

;; Replace "yes or no" with y or n
(defun yes-or-no-p (arg)
  "An alias for y-or-n-p, because I hate having to type 'yes' or 'no'."
  (y-or-n-p arg))

;; Put as much syntax highlighting into documents as possible
(setq font-lock-maximum-decoration t)

;; Turn on mouse wheel
(mouse-wheel-mode t)

;; show column number in status bar
(setq column-number-mode t)

;; arg >= 1 enable the menu bar. Menu bar is the File, Edit, Options,
;; Buffers, Tools, Emacs-Lisp, Help
(menu-bar-mode 0)

;; With numeric ARG, display the tool bar if and only if ARG is
;; positive.  Tool bar has icons document (read file), folder (read
;; directory), X (discard buffer), disk (save), disk+pen (save-as),
;; back arrow (undo), scissors (cut), etc.
(tool-bar-mode 0)

(setq auto-mode-alist (cons '("\\.pkg$" . sql-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\.vw$" . sql-mode) auto-mode-alist))
(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 )
(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 )

;; default to better frame titles
(setq frame-title-format
      (concat  "%b - emacs@" (system-name)))

;; always end a file with a newline
(setq require-final-newline 'query)
