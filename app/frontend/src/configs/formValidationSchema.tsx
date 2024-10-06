import * as Yup from "yup";

export const formValidation = {
  loginValidationSchema: Yup.object({
    password: Yup.string()
      .max(15, "Must be 15 characters or less")
      .required("Required"),
    email: Yup.string().email("Invalid email address").required("Required"),
  }),
};
