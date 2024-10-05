"use client";

import { FC, ReactNode } from "react";

interface ButtonProps {
  onClick?: () => void;
  variant?: "primary" | "secondary";
  disabled?: boolean;
  children: ReactNode; // Add children prop to the interface
}

const Button: FC<ButtonProps> = ({
  onClick,
  variant = "primary",
  disabled = false,
  children, // Destructure children here
}) => {
  const baseClasses = `h-8 px-2 py-1 w-full text-sm rounded-sm text-seasalt hover:bg-beige active:blur-sm transition duration-100`;
  const variantClasses = {
    primary: "bg-pakistan",
    secondary: "bg-sage",
  };

  return (
    <button
      onClick={onClick}
      type="button"
      className={`${baseClasses} ${variantClasses[variant]} ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
