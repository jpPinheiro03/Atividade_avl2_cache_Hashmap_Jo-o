package school.sptech.dto;

import jakarta.validation.constraints.NotBlank;

public record ConteudoRequest(
        @NotBlank String titulo,
        @NotBlank String corpo,
        @NotBlank String autor) {
}
