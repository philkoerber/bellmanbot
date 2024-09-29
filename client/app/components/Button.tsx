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
  const baseClasses = `px-2 py-1 text-sm rounded-sm text-seasalt hover:bg-beige active:blur-sm transition duration-100 w-fit`;
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
      {children} {/* Use children here */}
    </button>
  );
};

export default Button;
