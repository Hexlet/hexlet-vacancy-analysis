import { BrowserRouter } from 'react-router-dom';
import Header from './components/Layout/Header/Header';
import Footer from './components/Layout/Footer/Footer';
import { renderRoutes } from './routes';

function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow ">
          {renderRoutes()}
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App