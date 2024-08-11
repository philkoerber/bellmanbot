"use client";

import { FC } from "react";

interface ButtonProps {
  text: string;
  onClick?: () => void;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

const Button: FC<ButtonProps> = ({
  text,
  onClick,
  variant = "primary",
  disabled = false,
}) => {
  const baseClasses = `px-4 py-2 font-semibold rounded-sm text-seasalt hover:bg-beige active:blur-sm transition duration-100`;
  const variantClasses = {
    primary: "bg-pakistan",
    secondary: "bg-sage",
  };

  return (
    <button
      onClick={onClick}
      type={"button"}
      className={`${baseClasses} ${variantClasses[variant]} ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`}
      disabled={disabled}>
      {text}
    </button>
  );
};

export default Button;
