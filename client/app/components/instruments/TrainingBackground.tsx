const TrainingBackground = () => {
  return (
    <div className="w-[150vw] h-[150vh] max-h-[150vh] max-w-[150vw] aspect-square rounded-full bg-gradient-to-r from-pakistan to-beige animate-[spin_5s_linear_infinite] mx-auto transition-opacity duration-1000 opacity-0 animate-fade-in">
      <style jsx>{`
        @keyframes fade-in {
          0% {
            opacity: 0;
          }
          100% {
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
};

export default TrainingBackground;
