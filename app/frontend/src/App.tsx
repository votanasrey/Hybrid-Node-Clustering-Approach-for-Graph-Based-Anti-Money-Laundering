import {
  Route,
  BrowserRouter as Router,
  Routes,
  useLocation,
  Navigate,
} from "react-router-dom";
import Cookies from "js-cookie";
import { EAppRoutes, ECookies } from "./configs/constants";
import Layout from "./components/Layout";
import Login from "./routes/login";
import Dashboard from "./routes/dashboard";

function RequiredAuth({ children }: { children: React.ReactNode }) {
  const isAuthenticated = Cookies.get(ECookies.AUTH_TOKEN);

  const location = useLocation();
  return isAuthenticated ? (
    <Layout>{children}</Layout>
  ) : (
    <Navigate
      to={EAppRoutes.LOGIN}
      replace
      state={{ path: location.pathname }}
    />
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path={EAppRoutes.DASHBOARD}
          element={
            <RequiredAuth>
              <Dashboard />
            </RequiredAuth>
          }
        />
        <Route path={EAppRoutes.LOGIN} element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
